import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from langdetect import detect
from openai import OpenAI

# Load environment variables
load_dotenv()

# Validate env variables
mongo_uri = os.getenv("MONGO_URI")
openai_key = os.getenv("OPENAI_KEY")
if not mongo_uri or not openai_key:
    raise EnvironmentError("Missing MONGO_URI or OPENAI_KEY in .env")

# MongoDB setup
client = MongoClient(mongo_uri)
db = client["Verkkokauppa"]
collections = {
    "cpu": db["cpu"],
    "gpu": db["gpu"],
    "mobo": db["mobo"],
    "ram": db["rams"]
}
faq_collection = db["Chatbot"]
log_collection = db["conversation_logs"]

# OpenAI setup
openai = OpenAI(api_key=openai_key)

conversation_history = []
last_product_name = None
MAX_HISTORY = 6

SUPPORTED_LANGUAGES = ["fi", "en", "sv", "de", "fr", "es"]


def get_faq_context(limit=30):
    faqs = faq_collection.find({"answer": {"$exists": True}}).limit(limit)
    return "\n".join(f"{faq['question']}: {faq['answer']}" for faq in faqs)


def find_product_info(product_name):
    for col in collections.values():
        product = col.find_one({"name": {"$regex": product_name, "$options": "i"}})
        if product:
            return product
    return None


def format_price_and_warranty(product, lang):
    lang = lang if lang in SUPPORTED_LANGUAGES else "en"
    name = product.get("name", "")
    price = product.get("Price", {}).get("totalPrice")
    warranty = product.get("Warranty")

    messages = {
        "fi": (f"Tuotteen '{name}' hinta on {price} €.", f"Takuu: {warranty} vuotta."),
        "en": (f"The price of '{name}' is {price} €.", f"Warranty: {warranty} years."),
        "sv": (f"Priset för '{name}' är {price} €.", f"Garanti: {warranty} år."),
        "de": (f"Der Preis für '{name}' beträgt {price} €.", f"Garantie: {warranty} Jahre."),
        "fr": (f"Le prix de '{name}' est de {price} €.", f"Garantie : {warranty} ans."),
        "es": (f"El precio de '{name}' es {price} €.", f"Garantía: {warranty} años.")
    }

    return " ".join(msg for msg in messages[lang] if msg and price and warranty)


def chat_with_gpt(user_input):
    global last_product_name, conversation_history

    language = detect(user_input)
    context = get_faq_context()
    keywords = ["hinta", "maksaa", "price", "cost", "garanti", "warranty", "takuu"]

    matched_product = None
    for col in collections.values():
        matched_product = col.find_one({"name": {"$regex": user_input, "$options": "i"}})
        if matched_product:
            last_product_name = matched_product["name"]
            break

    if any(word in user_input.lower() for word in keywords):
        product = matched_product or find_product_info(last_product_name)
        if product:
            response = format_price_and_warranty(product, language)
        else:
            fallback = {
                "fi": "Valitettavasti en löytänyt tuotetietoja.",
                "en": "Unfortunately, I couldn't find the product information."
            }
            response = fallback.get(language, fallback["en"])
    elif "show all rams" in user_input.lower() or "näytä kaikki muistit" in user_input.lower():
        all_rams = list(collections["ram"].find())
        if not all_rams:
            return "RAM-muisteja ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {ram.get('name', 'Tuntematon')}, Hinta: {ram.get('Price', {}).get('totalPrice', 'ei tiedossa')} €, Takuu: {ram.get('Warranty', 'ei tiedossa')} vuotta"
            for ram in all_rams
        )
    else:
        system_prompt = [
            {"role": "system", "content":
                                        "Olet kohtelias asiakaspalvelurobotti, joka auttaa verkkokaupan asiakkaita."
                                        "Verkkokauppa myy tietokonekomponentteja, kuten RAM-muisteja, prosessoreita, näytönohjaimia ja emolevyjä."
                                        "Vastaa täsmällisesti, ystävällisesti ja ytimekkäästi asiakkaan kielellä. "
                                        "Jos asiakas kysyy hinnasta tai takuusta, ohjaa logiikka käyttämään tietokannan tietoja."
                                        "Käytä kohteliasta sävyä ja älä keksimällä keksi teknisiä tietoja, jos niitä ei ole annettu."},
            {"role": "system", "content": f"Tässä on usein kysyttyjä kysymyksiä:\n{context}"},
        ]
        messages = system_prompt + conversation_history[-MAX_HISTORY:] + [{"role": "user", "content": user_input}]

        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        response = completion.choices[0].message.content.strip()

    conversation_history += [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": response}
    ]
    conversation_history = conversation_history[-MAX_HISTORY:]

    log_collection.insert_one({
        "timestamp": datetime.now(),
        "question": user_input,
        "response": response,
        "language": language
    })

    return response