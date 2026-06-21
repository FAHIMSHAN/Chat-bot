from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()

print("KEY:", os.getenv("OPENAI_API_KEY")[:15])

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

try:
    response = client.models.list()
    print("SUCCESS")
except Exception as e:
    print("ERROR:", e)

    