import re
import os
import pandas as pd


def syllabus_intent(query):

    keywords = [
        "syllabus",
        "curriculum",
        "modules",
        "chapter",
        "chapters",
        "topics",
        "course content",
        "study plan"
    ]

    query = query.lower()

    return any(
        keyword in query
        for keyword in keywords
    )


def extract_phone(text):

    match = re.search(
        r"\d{10}",
        text
    )

    return match.group() if match else None


def extract_email(text):

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group() if match else None


def save_lead(
    name,
    phone,
    email,
    course
):

    row = {
        "Name": name,
        "Phone": phone,
        "Email": email,
        "Course": course
    }

    if os.path.exists("leads.csv"):

        df = pd.read_csv("leads.csv")

        df = pd.concat(
            [df, pd.DataFrame([row])],
            ignore_index=True
        )

    else:

        df = pd.DataFrame([row])

    df.to_csv(
        "leads.csv",
        index=False
    )