from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from pathlib import Path


DOCUMENTS_DIR = Path("documents")
DOCUMENTS_DIR.mkdir(exist_ok=True)

styles = getSampleStyleSheet()

title_style = ParagraphStyle(
    "TitleStyle",
    parent=styles["Title"],
    alignment=TA_CENTER,
    spaceAfter=20,
)

heading_style = ParagraphStyle(
    "HeadingStyle",
    parent=styles["Heading2"],
    spaceBefore=12,
    spaceAfter=8,
)

body_style = ParagraphStyle(
    "BodyStyle",
    parent=styles["BodyText"],
    leading=15,
    spaceAfter=8,
)


def create_pdf(filename, title, sections):

    path = DOCUMENTS_DIR / filename

    doc = SimpleDocTemplate(
        str(path),
        pagesize=letter,
        rightMargin=0.7 * inch,
        leftMargin=0.7 * inch,
        topMargin=0.7 * inch,
        bottomMargin=0.7 * inch,
    )

    content = []

    content.append(Paragraph(title, title_style))
    content.append(
        Paragraph(
            "Acme Technologies — Internal Policy Document",
            body_style,
        )
    )
    content.append(Spacer(1, 10))

    for heading, text in sections:

        content.append(
            Paragraph(heading, heading_style)
        )

        content.append(
            Paragraph(text, body_style)
        )

    doc.build(content)

    print(f"Created: {path}")


# --------------------------------------------------
# Employee Handbook
# --------------------------------------------------

employee_sections = [

    (
        "1. Working Hours",
        "Standard working hours are 9:00 AM to 6:00 PM from Monday to Friday. "
        "Employees are expected to complete eight working hours per day excluding "
        "the lunch break. Flexible working arrangements may be approved by the "
        "employee's reporting manager."
    ),

    (
        "2. Annual Leave",
        "Employees are entitled to 24 days of paid annual leave per calendar year. "
        "Employees may carry forward up to 10 unused leave days to the next "
        "calendar year."
    ),

    (
        "3. Sick Leave",
        "Employees receive 12 days of sick leave per calendar year. "
        "For sick leave lasting more than three consecutive working days, "
        "the employee may be required to provide appropriate medical documentation."
    ),

    (
        "4. Work From Home",
        "Employees may request work-from-home arrangements subject to manager "
        "approval. Employees working remotely must remain available during "
        "normal working hours and maintain access to required company systems."
    ),

    (
        "5. Leave Approval",
        "Leave requests longer than five consecutive working days require "
        "approval from the employee's reporting manager. Emergency leave should "
        "be communicated to the manager as soon as reasonably possible."
    ),

    (
        "6. Maternity and Paternity Leave",
        "Eligible employees may receive maternity or paternity leave according "
        "to applicable company policy and local employment regulations. "
        "Employees should contact Human Resources before planning extended leave."
    ),

    (
        "7. Employee Benefits",
        "Employees are eligible for health insurance, accidental insurance, "
        "and other benefits according to their employment grade and applicable "
        "company benefit plans."
    ),

    (
        "8. Workplace Conduct",
        "Employees are expected to maintain professional behavior, respect "
        "colleagues, protect confidential information, and comply with company "
        "policies. Harassment, discrimination, and unauthorized disclosure of "
        "company information are prohibited."
    ),

    (
        "9. Performance Reviews",
        "Employees participate in periodic performance reviews. Performance "
        "reviews may consider project delivery, technical contribution, "
        "collaboration, communication, and adherence to company policies."
    ),
]


# --------------------------------------------------
# Travel Policy
# --------------------------------------------------

travel_sections = [

    (
        "1. Business Travel",
        "Employees may travel for approved business purposes including client "
        "meetings, conferences, training, and project activities. Business travel "
        "must normally receive manager approval before booking."
    ),

    (
        "2. Domestic Flight Travel",
        "Domestic economy-class airfare is reimbursable for approved business "
        "travel. Employees should select reasonably priced routes and book "
        "through the company's approved travel process whenever available."
    ),

    (
        "3. Hotel Accommodation",
        "For domestic business travel, employees may claim hotel accommodation "
        "up to INR 6,000 per night. Any amount above the approved limit requires "
        "prior authorization from the reporting manager."
    ),

    (
        "4. International Accommodation",
        "International hotel expenses are reimbursed up to the applicable "
        "destination-specific limit established by the company. Employees should "
        "select reasonably priced accommodation close to the business location."
    ),

    (
        "5. Meals",
        "Employees traveling domestically may claim meal expenses up to INR 1,200 "
        "per day. Original receipts should be retained where required by the "
        "expense management process."
    ),

    (
        "6. Local Transportation",
        "Reasonable taxi, public transportation, and approved local travel "
        "expenses incurred for business purposes are reimbursable. Personal "
        "transportation expenses are not reimbursable."
    ),

    (
        "7. Travel Advance",
        "Employees may request a travel advance before an approved business trip. "
        "Unused advance amounts must be returned or reconciled through the "
        "expense management system."
    ),

    (
        "8. Expense Submission",
        "Travel expenses should normally be submitted within 15 calendar days "
        "after returning from the business trip. Expense claims should include "
        "receipts and the relevant business purpose."
    ),

    (
        "9. Prohibited Expenses",
        "Personal entertainment, minibar charges, personal shopping, traffic "
        "fines, and expenses for non-business companions are not reimbursable "
        "unless explicitly approved by the company."
    ),
]


# --------------------------------------------------
# IT Security Policy
# --------------------------------------------------

security_sections = [

    (
        "1. Password Requirements",
        "Employees must use strong passwords containing a combination of "
        "uppercase letters, lowercase letters, numbers, and special characters. "
        "Passwords must not be shared with other employees."
    ),

    (
        "2. Multi-Factor Authentication",
        "Multi-factor authentication is mandatory for systems that support MFA. "
        "Employees must use the company-approved authentication mechanism."
    ),

    (
        "3. VPN Usage",
        "Employees accessing internal company resources from an external network "
        "must use the approved company VPN when required. VPN credentials must "
        "never be shared with another person."
    ),

    (
        "4. Phishing Emails",
        "Employees must not click suspicious links, download unexpected "
        "attachments, or provide credentials in response to unsolicited emails. "
        "Suspicious messages should be reported to the IT security team."
    ),

    (
        "5. Data Protection",
        "Confidential company information must only be stored on approved "
        "company systems. Employees must not transfer confidential information "
        "to personal cloud storage or unauthorized external services."
    ),

    (
        "6. Device Security",
        "Company laptops must be protected with a password or approved "
        "authentication mechanism. Employees must lock their devices when "
        "leaving them unattended."
    ),

    (
        "7. Security Incidents",
        "Security incidents including suspected malware infections, lost devices, "
        "credential theft, or unauthorized access must be reported to the IT "
        "security team as soon as possible."
    ),

    (
        "8. Software Installation",
        "Employees must not install unauthorized or pirated software on company "
        "devices. Software required for business purposes should be obtained "
        "through approved channels."
    ),

    (
        "9. Remote Work Security",
        "Employees working remotely must use secure networks and follow company "
        "security procedures. Confidential information should not be displayed "
        "where unauthorized individuals can view it."
    ),
]


# --------------------------------------------------
# Generate PDFs
# --------------------------------------------------

create_pdf(
    "employee_handbook.pdf",
    "Employee Handbook",
    employee_sections,
)

create_pdf(
    "travel_policy.pdf",
    "Business Travel Policy",
    travel_sections,
)

create_pdf(
    "it_security_policy.pdf",
    "IT Security Policy",
    security_sections,
)

print("\nAll enterprise policy PDFs created successfully.")
