from openai import OpenAI
import os
from dotenv import load_dotenv


load_dotenv()
openai_api_key = os.getenv("OPENAI_KEY")
openai = OpenAI(api_key=openai_api_key)

def chat_with_gpt(user_input):
    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful customer service bot who answers politely to customers' questions."},
            {"role": "user", "content": user_input}
        ]
    )
    return response.choices[0].message.content.strip()

