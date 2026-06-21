from fastapi import FastAPI
from pydantic import BaseModel

from rag_search import search_courses
from gpt_model import generate_response

from lead_manager import (
    syllabus_intent,
    extract_phone,
    extract_email,
    save_lead
)

app = FastAPI(
    title="EduPlatform Chatbot API"
)

user_state = {}

GREETINGS = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening"
]


class ChatRequest(BaseModel):
    user_id: str
    message: str


@app.get("/")
def home():

    return {
        "message":
        "EduPlatform Chatbot API Running"
    }


@app.post("/chat")
def chat(request: ChatRequest):

    user_id = request.user_id
    message = request.message.strip()

    # Greeting

    if message.lower() in GREETINGS:

        return {
            "response":
            """
Welcome to EduPlatform 🎓

I can help you explore:

📘 Classes 5–12 Courses
🎓 Undergraduate Programs
📚 Postgraduate Programs
🔬 PhD Programs

Tell me the course or subject you are interested in.
            """
        }

    # Waiting for Contact Details

    if (
        user_id in user_state and
        user_state[user_id]["state"] == "waiting_contact"
    ):

        phone = extract_phone(message)
        email = extract_email(message)

        lines = [
            line.strip()
            for line in message.split("\n")
            if line.strip()
        ]

        name = lines[0] if lines else ""

        if phone and email:

            course_name = (
                user_state[user_id]["course"]
            )

            save_lead(
                name,
                phone,
                email,
                course_name
            )

            user_state.pop(
                user_id,
                None
            )

            return {
                "response":
                f"""
Thank you {name}.

Your request for:

{course_name}

has been successfully submitted.

An EduPlatform Academic Counselor will contact you shortly and explain the complete syllabus, learning outcomes, and enrollment process.
                """
            }

        return {
            "response":
            """
Please provide:

Full Name
Mobile Number
Email Address

Example:

John Doe
9876543210
john@gmail.com
            """
        }

    # Syllabus Request

    if syllabus_intent(message):

        results = search_courses(
            message,
            top_k=1
        )

        if results:

            course_name = results[0]["Course Name"]

            user_state[user_id] = {
                "state": "waiting_contact",
                "course": course_name
            }

            return {
                "response":
                f"""
Detailed syllabus information for:

{course_name}

is handled by our Academic Counseling Team.

Please provide:

• Full Name
• Mobile Number
• Email Address

Our team will contact you shortly.
                """
            }

        return {
            "response":
            """
Please specify the course name whose syllabus you need.
            """
        }

    # Course Search

    results = search_courses(
        message
    )

    response = generate_response(
        message,
        results
    )

    return {
        "response": response
    }