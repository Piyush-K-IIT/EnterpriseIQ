import os
from pathlib import Path
from typing import Annotated

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import (
    HumanMessage,
    SystemMessage,
)

from langgraph.graph import StateGraph, START
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition

from typing_extensions import TypedDict

try:
    from app.tools import calculate, create_support_ticket
    from app.rag_tool import search_documents
except ModuleNotFoundError:
    from tools import calculate, create_support_ticket
    from rag_tool import search_documents


# =========================================================
# PROJECT PATHS
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv(
    PROJECT_ROOT / ".env"
)

api_key = os.getenv(
    "GEMINI_API_KEY"
)

if not api_key:
    raise ValueError(
        "GEMINI_API_KEY not found in .env"
    )


# =========================================================
# GEMINI
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    api_key=api_key,
)


# =========================================================
# TOOLS
# =========================================================

tools = [
    search_documents,
    calculate,
    create_support_ticket,
]

llm_with_tools = llm.bind_tools(
    tools
)


# =========================================================
# STATE
# =========================================================

class AgentState(TypedDict):

    messages: Annotated[
        list,
        add_messages
    ]


# =========================================================
# AGENT NODE
# =========================================================

def agent_node(
    state: AgentState
):

    response = llm_with_tools.invoke(
        state["messages"]
    )

    return {
        "messages": [
            response
        ]
    }


# =========================================================
# LANGGRAPH
# =========================================================

graph_builder = StateGraph(
    AgentState
)

graph_builder.add_node(
    "agent",
    agent_node
)

graph_builder.add_node(
    "tools",
    ToolNode(tools)
)

graph_builder.add_edge(
    START,
    "agent"
)

graph_builder.add_conditional_edges(
    "agent",
    tools_condition
)

graph_builder.add_edge(
    "tools",
    "agent"
)

agent = graph_builder.compile()


# =========================================================
# CONTENT EXTRACTION
# =========================================================

def extract_text(content):

    if isinstance(
        content,
        str
    ):
        return content

    if isinstance(
        content,
        list
    ):

        parts = []

        for item in content:

            if isinstance(
                item,
                dict
            ):

                if item.get(
                    "type"
                ) == "text":

                    parts.append(
                        item.get(
                            "text",
                            ""
                        )
                    )

            elif isinstance(
                item,
                str
            ):

                parts.append(
                    item
                )

        return "\n".join(
            parts
        )

    return str(content)


# =========================================================
# SOURCE EXTRACTION
# =========================================================

def extract_sources(
    messages
):

    sources = []

    for message in messages:

        content = extract_text(
            getattr(
                message,
                "content",
                ""
            )
        )

        if not content:
            continue

        lines = content.splitlines()

        for i, line in enumerate(
            lines
        ):

            line = line.strip()

            if not line.startswith(
                "[SOURCE"
            ):
                continue

            # ---------------------------------------------
            # The source location is the next line
            # ---------------------------------------------

            for j in range(
                i + 1,
                len(lines)
            ):

                candidate = (
                    lines[j].strip()
                )

                if not candidate:
                    continue

                if candidate.startswith(
                    "Similarity Score:"
                ):
                    continue

                if candidate == "---":
                    continue

                if (
                    ".pdf" in candidate
                    or ".txt" in candidate
                ):

                    if candidate not in sources:

                        sources.append(
                            candidate
                        )

                    break

    return sources


# =========================================================
# TOOL EXTRACTION
# =========================================================

def extract_tools(
    messages
):

    tools_used = []

    for message in messages:

        # ---------------------------------------------
        # LangChain tool_calls
        # ---------------------------------------------

        tool_calls = getattr(
            message,
            "tool_calls",
            None
        )

        if tool_calls:

            for call in tool_calls:

                name = call.get(
                    "name"
                )

                if (
                    name
                    and name not in tools_used
                ):

                    tools_used.append(
                        name
                    )

        # ---------------------------------------------
        # Fallback: additional_kwargs
        # ---------------------------------------------

        additional_kwargs = getattr(
            message,
            "additional_kwargs",
            {}
        )

        if additional_kwargs:

            tool_calls = (
                additional_kwargs.get(
                    "tool_calls",
                    []
                )
            )

            for call in tool_calls:

                function = call.get(
                    "function",
                    {}
                )

                name = function.get(
                    "name"
                )

                if (
                    name
                    and name not in tools_used
                ):

                    tools_used.append(
                        name
                    )

    return tools_used


def ask_agent(question: str):

    system_message = SystemMessage(
        content="""
You are EnterpriseIQ, an enterprise knowledge
and support assistant.

IMPORTANT RULES:

1. Use the search_documents tool whenever the
   user's question could be answered using the
   indexed documents.

2. This includes questions about:
   - company policies
   - employee handbook
   - travel policies
   - IT security
   - leave
   - benefits
   - reimbursements
   - Applied Numerical Analysis
   - numerical methods
   - mathematical concepts contained in
     the indexed documents

3. Do NOT rely only on your internal knowledge
   when relevant information may exist in the
   indexed documents.

4. After using search_documents, answer the
   user's question using the retrieved context.

5. Do not invent information that is not supported
   by the retrieved documents.

6. Keep the answer clear and useful.

7. If the requested information cannot be found
   in the indexed documents, clearly say so.
"""
    )

    result = agent.invoke(
        {
            "messages": [
                system_message,
                HumanMessage(
                    content=question
                )
            ]
        }
    )

    messages = result["messages"]

    tools_used = extract_tools(
        messages
    )

    sources = extract_sources(
        messages
    )

    final_answer = ""

    for message in reversed(messages):

        content = extract_text(
            getattr(
                message,
                "content",
                ""
            )
        )

        if content.strip():

            final_answer = content.strip()

            break

    return {
        "answer": final_answer,
        "tools_used": tools_used,
        "sources": sources,
    }

    # -----------------------------------------------------
    # Extract tools
    # -----------------------------------------------------

    tools_used = extract_tools(
        messages
    )

    # -----------------------------------------------------
    # Extract sources
    # -----------------------------------------------------

    sources = extract_sources(
        messages
    )

    # -----------------------------------------------------
    # Final answer
    # -----------------------------------------------------

    final_answer = ""

    for message in reversed(
        messages
    ):

        content = extract_text(
            getattr(
                message,
                "content",
                ""
            )
        )

        if content.strip():

            final_answer = (
                content.strip()
            )

            break

    return {
        "answer": final_answer,
        "tools_used": tools_used,
        "sources": sources,
    }


# =========================================================
# TERMINAL APPLICATION
# =========================================================

if __name__ == "__main__":

    print(
        "\n======================================"
    )

    print(
        "      EnterpriseIQ AI Agent"
    )

    print(
        "======================================"
    )

    print(
        "\nAvailable tools:"
    )

    print(
        "1. Document Search"
    )

    print(
        "2. Calculator"
    )

    print(
        "3. Support Ticket"
    )

    print(
        "\nType 'exit' to quit.\n"
    )

    while True:

        question = input(
            "You: "
        )

        if question.lower() == "exit":

            break

        try:

            result = ask_agent(
                question
            )

            print(
                "\nEnterpriseIQ:"
            )

            print(
                result["answer"]
            )

            if result[
                "tools_used"
            ]:

                print(
                    "\nTools used: "
                    + ", ".join(
                        result[
                            "tools_used"
                        ]
                    )
                )

            if result[
                "sources"
            ]:

                print(
                    "\nSources:"
                )

                for source in result[
                    "sources"
                ]:

                    print(
                        "- " + source
                    )

            print()

        except Exception as e:

            print(
                "\nError:"
            )

            print(e)

            print()