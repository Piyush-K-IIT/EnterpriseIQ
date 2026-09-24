from langchain_core.tools import tool
import ast
import operator


# Allowed mathematical operators
_ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
}


@tool
def calculate(expression: str) -> str:
    """
    Calculate a mathematical expression.

    Use this tool when the user asks for arithmetic or numerical calculations.
    Example: 6000 * 3 or 1200 / 2.
    """
    try:
        tree = ast.parse(expression, mode="eval")

        def evaluate(node):
            if isinstance(node, ast.Constant):
                if isinstance(node.value, (int, float)):
                    return node.value
                raise ValueError("Invalid number.")

            if isinstance(node, ast.BinOp):
                operation = _ALLOWED_OPERATORS.get(type(node.op))

                if operation is None:
                    raise ValueError("Operator not allowed.")

                return operation(
                    evaluate(node.left),
                    evaluate(node.right)
                )

            raise ValueError("Invalid expression.")

        result = evaluate(tree.body)

        return str(result)

    except Exception as e:
        return f"Calculation error: {e}"


@tool
def create_support_ticket(issue: str) -> str:
    """
    Create a support ticket for an employee issue.

    Use this tool when the user explicitly asks to create, raise,
    or submit a support ticket.
    """

    ticket_id = "TKT-1001"

    return (
        f"Support ticket created successfully.\n"
        f"Ticket ID: {ticket_id}\n"
        f"Issue: {issue}\n"
        f"Status: Open"
    )
