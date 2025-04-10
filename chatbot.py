from openai import OpenAI
import os
from dotenv import load_dotenv
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
db = client["Verkkokauppa"]
collection = db["Chatbot"]

openai_api_key = os.getenv("OPENAI_KEY")
openai = OpenAI(api_key=openai_api_key)

def get_faq_context():
    faqs = collection.find({"answer": {"$exists": True}})
    return "\n".join(f"{faq['question']}: {faq['answer']}" for faq in faqs)

def chat_with_gpt(user_input):

    collection.insert_one({
        "question": user_input
    })

    context = get_faq_context()
    conversation = [
        {"role": "system", "content": "You are a helpful customer service bot who answers politely to customers' questions."},
        {"role": "system", "content": f"Here are some FAQs:\n{context}"},
        {"role": "user", "content": user_input}
    ]

    response = openai.chat.completions.create(
        model="gpt-4o-mini",
        messages=conversation
            
    )
    
    return response.choices[0].message.content.strip()

