import re
from typing import TypedDict

from langgraph.graph import StateGraph, START, END


class EmailState(TypedDict):
    email: str
    category: str
    priority: str
    action: str
    tasks: str
    deadline: str
    reply: str


# -----------------------------
# Agent 1: Email Understanding
# -----------------------------

def understand_email(state: EmailState):

    email = state["email"].lower()

    if any(word in email for word in [
        "interview",
        "job",
        "offer",
        "recruitment",
        "hiring"
    ]):
        category = "Career / Recruitment"

    elif any(word in email for word in [
        "meeting",
        "project",
        "deadline",
        "client",
        "work"
    ]):
        category = "Work"

    elif any(word in email for word in [
        "payment",
        "invoice",
        "transaction",
        "refund"
    ]):
        category = "Finance"

    elif any(word in email for word in [
        "sale",
        "discount",
        "offer",
        "promotion"
    ]):
        category = "Promotion"

    else:
        category = "General"

    return {
        "category": category
    }


# -----------------------------
# Agent 2: Priority Detection
# -----------------------------

def detect_priority(state: EmailState):

    email = state["email"].lower()

    high_words = [
        "urgent",
        "immediately",
        "today",
        "interview",
        "deadline",
        "important",
        "action required"
    ]

    medium_words = [
        "tomorrow",
        "meeting",
        "please confirm",
        "response required",
        "follow up"
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


# -----------------------------
# Agent 3: Action Decision
# -----------------------------

def decide_action(state: EmailState):

    email = state["email"].lower()

    reply_words = [
        "please confirm",
        "please reply",
        "let me know",
        "can you",
        "could you",
        "please respond",
        "confirmation required"
    ]

    followup_words = [
        "follow up",
        "follow-up",
        "reminder"
    ]

    if any(word in email for word in reply_words):
        action = "Reply Required"

    elif any(word in email for word in followup_words):
        action = "Follow-up Required"

    else:
        action = "No Action Required"

    return {
        "action": action
    }


# -----------------------------
# Agent 4: Task Extraction
# -----------------------------

def extract_tasks(state: EmailState):

    email = state["email"]

    task_words = [
        "please",
        "confirm",
        "submit",
        "send",
        "complete",
        "attend",
        "review",
        "respond"
    ]

    sentences = re.split(r"[.!?]", email)

    tasks = []

    for sentence in sentences:

        sentence_lower = sentence.lower()

        if any(word in sentence_lower for word in task_words):

            cleaned = sentence.strip()

            if cleaned:
                tasks.append(cleaned)

    if tasks:
        task_text = "\n".join(
            f"- {task}" for task in tasks
        )
    else:
        task_text = "No specific task detected."

    return {
        "tasks": task_text
    }


# -----------------------------
# Agent 5: Deadline Detection
# -----------------------------

def detect_deadline(state: EmailState):

    email = state["email"].lower()

    if "today" in email:
        deadline = "Today"

    elif "tomorrow" in email:
        deadline = "Tomorrow"

    elif "next week" in email:
        deadline = "Next week"

    else:

        date_pattern = r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b"

        match = re.search(date_pattern, email)

        if match:
            deadline = match.group()

        else:
            deadline = "No deadline detected."

    return {
        "deadline": deadline
    }


# -----------------------------
# Agent 6: Reply Generator
# -----------------------------

def generate_reply(state: EmailState):

    if state["action"] == "No Action Required":

        reply = "No reply required."

    elif state["category"] == "Career / Recruitment":

        reply = (
            "Thank you for the information. "
            "I acknowledge the email and confirm my availability."
        )

    elif state["category"] == "Work":

        reply = (
            "Thank you for the update. "
            "I acknowledge the request and will take the necessary action."
        )

    else:

        reply = (
            "Thank you for your email. "
            "I have received the information and will get back to you shortly."
        )

    return {
        "reply": reply
    }


# -----------------------------
# LangGraph Workflow
# -----------------------------

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


email_agent = workflow.compile()


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
