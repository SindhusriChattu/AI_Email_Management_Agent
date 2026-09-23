import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


# =========================================================
# EMAIL STATE
# =========================================================

class EmailState(TypedDict):
    email: str
    category: str
    priority: str
    action: str
    tasks: str
    deadline: str
    reply: str


# =========================================================
# AGENT 1: UNDERSTAND EMAIL
# =========================================================

def understand_email(state: EmailState):

    email = state["email"].lower()

    # Training / sessions
    if any(word in email for word in [
        "training",
        "skills session",
        "practical skills session",
        "live interactive",
        "workshop",
        "mandatory to attend",
        "session details"
    ]):
        category = "Training / Skills Session"

    # Career / recruitment
    elif any(word in email for word in [
        "interview",
        "job",
        "offer",
        "recruitment",
        "hiring",
        "selection process"
    ]):
        category = "Career / Recruitment"

    # Meetings / work
    elif any(word in email for word in [
        "meeting",
        "project",
        "client",
        "work"
    ]):
        category = "Work"

    # Finance
    elif any(word in email for word in [
        "payment",
        "invoice",
        "transaction",
        "refund"
    ]):
        category = "Finance"

    # Promotions
    elif any(word in email for word in [
        "sale",
        "discount",
        "promotion"
    ]):
        category = "Promotion"

    else:
        category = "General"

    return {
        "category": category
    }


# =========================================================
# AGENT 2: PRIORITY DETECTION
# =========================================================

def detect_priority(state: EmailState):

    email = state["email"].lower()

    high_words = [
        "urgent",
        "immediately",
        "today",
        "interview",
        "deadline",
        "important",
        "action required",
        "mandatory",
        "without fail",
        "selection process"
    ]

    medium_words = [
        "tomorrow",
        "meeting",
        "please confirm",
        "response required",
        "follow up",
        "register"
    ]

    if any(word in email for word in high_words):
        priority = "HIGH"

    elif any(word in email for word in medium_words):
        priority = "MEDIUM"

    else:
        priority = "LOW"

    return {
        "priority": priority
    }


# =========================================================
# AGENT 3: ACTION DECISION
# =========================================================

def decide_action(state: EmailState):

    email = state["email"].lower()

    # Registration / attendance
    if any(word in email for word in [
        "register in advance",
        "please register",
        "register",
        "attendance is mandatory",
        "attend both sessions",
        "please make sure to register",
        "attend without fail"
    ]):
        action = "Register & Attend"

    # Reply required
    elif any(word in email for word in [
        "please confirm",
        "please reply",
        "let me know",
        "can you",
        "could you",
        "please respond",
        "confirmation required"
    ]):
        action = "Reply Required"

    # Follow-up
    elif any(word in email for word in [
        "follow up",
        "follow-up",
        "reminder"
    ]):
        action = "Follow-up Required"

    else:
        action = "No Action Required"

    return {
        "action": action
    }


# =========================================================
# AGENT 4: TASK EXTRACTION
# =========================================================

def extract_tasks(state: EmailState):

    email = state["email"].lower()

    tasks = []

    # Registration
    if "register" in email:
        tasks.append("Register for the session")

    # Attendance
    if "attendance is mandatory" in email or "attend both sessions" in email:
        tasks.append("Attend both sessions")

    # Preparation
    if "prepare" in email:
        tasks.append("Prepare the required topics")

    # Confirmation
    if "please confirm" in email:
        tasks.append("Confirm attendance")

    # Submission
    if "submit" in email:
        tasks.append("Submit the required information")

    # Review
    if "review" in email:
        tasks.append("Review the provided information")

    if tasks:

        task_text = "\n".join(
            f"• {task}" for task in tasks
        )

    else:

        task_text = "No specific task detected."

    return {
        "tasks": task_text
    }
# =========================================================
# AGENT 5: DEADLINE DETECTION
# =========================================================

def detect_deadline(state: EmailState):

    email = state["email"].lower()

    # Specific date range
    if "23rd & 24th september 2026" in email:

        deadline = "23rd & 24th September 2026"

    elif "23rd and 24th september 2026" in email:

        deadline = "23rd & 24th September 2026"

    elif "today" in email:

        deadline = "Today"

    elif "tomorrow" in email:

        deadline = "Tomorrow"

    elif "next week" in email:

        deadline = "Next week"

    else:

        date_pattern = (
            r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"
        )

        match = re.search(
            date_pattern,
            email
        )

        if match:

            deadline = match.group()

        else:

            # Detect month + year/date formats
            month_pattern = (
                r"\b\d{1,2}(?:st|nd|rd|th)?\s+"
                r"(?:january|february|march|april|may|june|"
                r"july|august|september|october|november|december)"
                r"(?:\s+\d{4})?"
            )

            match = re.search(
                month_pattern,
                email
            )

            if match:
                deadline = match.group()
            else:
                deadline = "No deadline detected."

    return {
        "deadline": deadline
    }


# =========================================================
# AGENT 6: REPLY GENERATOR
# =========================================================

def generate_reply(state: EmailState):

    action = state["action"]
    category = state["category"]

    # No reply needed
    if action == "No Action Required":

        reply = "No reply required."

    # Registration/attendance emails
    elif action == "Register & Attend":

        reply = (
            "Thank you for the information. "
            "I will register for the session and attend "
            "the scheduled sessions."
        )

    # Career emails
    elif category == "Career / Recruitment":

        reply = (
            "Thank you for the information. "
            "I acknowledge the email and confirm my availability."
        )

    # Work emails
    elif category == "Work":

        reply = (
            "Thank you for the update. "
            "I acknowledge the request and will take "
            "the necessary action."
        )

    # General reply
    else:

        reply = (
            "Thank you for your email. "
            "I have received the information and "
            "will take the necessary action."
        )

    return {
        "reply": reply
    }


# =========================================================
# LANGGRAPH WORKFLOW
# =========================================================

workflow = StateGraph(EmailState)

workflow.add_node(
    "understand_email",
    understand_email
)

workflow.add_node(
    "detect_priority",
    detect_priority
)

workflow.add_node(
    "decide_action",
    decide_action
)

workflow.add_node(
    "extract_tasks",
    extract_tasks
)

workflow.add_node(
    "detect_deadline",
    detect_deadline
)

workflow.add_node(
    "generate_reply",
    generate_reply
)


# Workflow sequence

workflow.add_edge(
    START,
    "understand_email"
)

workflow.add_edge(
    "understand_email",
    "detect_priority"
)

workflow.add_edge(
    "detect_priority",
    "decide_action"
)

workflow.add_edge(
    "decide_action",
    "extract_tasks"
)

workflow.add_edge(
    "extract_tasks",
    "detect_deadline"
)

workflow.add_edge(
    "detect_deadline",
    "generate_reply"
)

workflow.add_edge(
    "generate_reply",
    END
)


# Compile agent

email_agent = workflow.compile()


# =========================================================
# MAIN FUNCTION
# =========================================================

def process_email(email):

    result = email_agent.invoke({

        "email": email,

        "category": "",

        "priority": "",

        "action": "",

        "tasks": "",

        "deadline": "",

        "reply": ""
    })

    return result
