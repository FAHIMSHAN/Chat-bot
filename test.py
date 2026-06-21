from openai import OpenAI

client = OpenAI(
    api_key="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"
)

response = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "user", "content": "Hello"}
    ]
)

print(response.choices[0].message.content)