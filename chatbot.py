from openai import OpenAI
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime

# Load environment variables
load_dotenv()

# Set up MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client["Verkkokauppa"]
collection = db["Chatbot"]

# Set up OpenAI
openai_api_key = os.getenv("OPENAI_KEY")
openai = OpenAI(api_key=openai_api_key)

# Load FAQ context from database
def get_faq_context():
    faqs = collection.find({"answer": {"$exists": True}})
    return "\n".join(f"{faq['question']}: {faq['answer']}" for faq in faqs)

# Chat function
def chat_with_gpt(user_input):
    context = get_faq_context()

    messages = [
        {"role": "system", "content": "Olet kohtelias asiakaspalvelurobotti, joka auttaa verkkokaupan asiakkaita."},
        {"role": "system", "content": f"Tässä on usein kysyttyjä kysymyksiä:\n{context}"},
        {"role": "user", "content": user_input}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages
    )

    bot_response = response.choices[0].message.content.strip()

    # Save both question and response to MongoDB
    collection.insert_one({
        "timestamp": datetime.now(),
        "question": user_input,
        "response": bot_response
    })

    return bot_response