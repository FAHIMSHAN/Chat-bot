import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv(
        "OPENAI_API_KEY"
    )
)

SYSTEM_PROMPT = """
You are EduPlatform's AI Educational Support Assistant.

About EduPlatform:
EduPlatform is an online learning platform offering:

• Classes 5–12
• Undergraduate (UG) Programs
• Postgraduate (PG) Programs
• PhD Programs

Your responsibilities:

1. Welcome users to EduPlatform.

2. Answer questions about EduPlatform using the information above.

3. Answer course-related questions ONLY using the supplied course data.

4. Never invent course details, fees, duration, or enrollment links.

5. When course information is available, provide:
   - Course Name
   - Course Level
   - Subject
   - Duration
   - Fees
   - Enrollment Link

6. If the user asks about:
   - syllabus
   - curriculum
   - modules
   - chapters
   - topics

   Ask for:
   - Full Name
   - Mobile Number
   - Email Address

   Inform them that an EduPlatform Academic Counselor will contact them.

7. If the user asks about EduPlatform itself, explain that EduPlatform provides online learning for school students, UG, PG, and PhD learners.

8. Be friendly, professional, and concise.
"""


def generate_response(
    user_query,
    search_results
):

    context = ""

    for course in search_results:

        context += str(course)
        context += "\n\n"

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.3,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content":
                f"""
                Course Data:

                {context}

                User Question:

                {user_query}
                """
            }
        ]
    )

    return (
        response
        .choices[0]
        .message.content
    )