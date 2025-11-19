import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from langdetect import detect
from openai import OpenAI

# Load environment variables

load_dotenv()

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

# Conversation memory

conversation_history = []
last_product_name = None
MAX_HISTORY = 6

# Supported languages

SUPPORTED_LANGUAGES = ["fi", "en", "sv", "de", "fr", "es"]

# --- Utility Functions --- #

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


# --- Main Chat Function --- #

def chat_with_gpt(user_input):
    global last_product_name, conversation_history

    # Detect language

    language = detect(user_input)
    context = get_faq_context()

    # Define tech-related keywords

    tech_keywords = [
        "cpu", "gpu", "ram", "mobo", "motherboard", "graphics card", "processor",
        "computer", "pc", "ssd", "storage", "cooler", "power supply", "psu",
        "näytönohjain", "prosessori", "muisti", "tietokone", "kovalevy", "emolevy"
    ]

    # Filter non-tech questions

    if not any(word.lower() in user_input.lower() for word in tech_keywords):
        non_tech_responses = {
            "fi": "Voin auttaa vain tietokonekomponentteihin ja teknologiaan liittyvissä kysymyksissä.",
            "en": "I can only help with questions related to computer components or technology.",
            "sv": "Jag kan bara hjälpa till med frågor som rör datorer eller teknik.",
            "es": "Solo puedo ayudarte con preguntas relacionadas con componentes informáticos o tecnología.",
            "de": "Ich kann nur bei Fragen zu Computern oder Technologie helfen.",
            "fr": "Je peux uniquement vous aider avec des questions liées aux ordinateurs ou à la technologie."
        }
        return non_tech_responses.get(language, non_tech_responses["en"])

    # Keywords related to price and warranty

    keywords = ["hinta", "maksaa", "price", "cost", "garanti", "warranty", "takuu"]

    matched_product = None
    for col in collections.values():
        matched_product = col.find_one({"name": {"$regex": user_input, "$options": "i"}})
        if matched_product:
            last_product_name = matched_product["name"]
            break

    # --- Price / Warranty Queries --- #

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

    # --- "Show all" Queries --- #

    elif any(cmd in user_input.lower() for cmd in ["show all rams", "näytä kaikki muistit"]):
        all_rams = list(collections["ram"].find())
        if not all_rams:
            return "RAM-muisteja ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {ram.get('name', 'Tuntematon')}, Hinta: {ram.get('Price', {}).get('totalPrice', 'ei tiedossa')} €, Takuu: {ram.get('Warranty', 'ei tiedossa')} vuotta"
            for ram in all_rams
        )

    elif any(cmd in user_input.lower() for cmd in ["show all cpus", "näytä kaikki prosessorit"]):
        all_cpus = list(collections["cpu"].find())
        if not all_cpus:
            return "Prosessoreita ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {cpu.get('name', 'Tuntematon')}, Hinta: {cpu.get('Price', {}).get('totalPrice', 'ei tiedossa')} €, Takuu: {cpu.get('Warranty', 'ei tiedossa')} vuotta"
            for cpu in all_cpus
        )

    elif any(cmd in user_input.lower() for cmd in ["show all gpus", "näytä kaikki näytönohjaimet"]):
        all_gpus = list(collections["gpu"].find())
        if not all_gpus:
            return "Näytönohjaimia ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {gpu.get('name', 'Tuntematon')}, Hinta: {gpu.get('Price', {}).get('totalPrice', 'ei tiedossa')} €, Takuu: {gpu.get('Warranty', 'ei tiedossa')} vuotta"
            for gpu in all_gpus
        )

    elif any(cmd in user_input.lower() for cmd in ["show all mobos", "näytä kaikki emolevyt", "show all motherboards"]):
        all_mobos = list(collections["mobo"].find())
        if not all_mobos:
            return "Emolevyjä ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {mobo.get('name', 'Tuntematon')}, Hinta: {mobo.get('Price', {}).get('totalPrice', 'ei tiedossa')} €, Takuu: {mobo.get('Warranty', 'ei tiedossa')} vuotta"
            for mobo in all_mobos
        )

    # --- Default GPT Response --- #
    else:
        prompts_by_lang = {
            "en": "You are a polite customer service assistant for an online electronics store. Only answer questions related to computer components, gaming PCs, or other tech-related topics. If the user asks about unrelated topics, politely refuse.",
            "fi": "Olet ystävällinen asiakaspalvelurobotti, joka auttaa asiakkaita tietokonekomponentteihin ja teknologiaan liittyvissä asioissa. Jos asiakas kysyy jotain, mikä ei liity teknologiaan, kieltäydy kohteliaasti.",
            "sv": "Du är en artig kundtjänstbot som endast svarar på frågor om datorer eller teknik. Om frågan inte handlar om teknik, vägra artigt.",
            "es": "Eres un asistente de atención al cliente para una tienda de informática. Solo respondes preguntas relacionadas con componentes informáticos o tecnología. Rechaza amablemente cualquier otro tema.",
            "de": "Du bist ein höflicher Kundenservice-Bot für ein Elektronikgeschäft. Antworte nur auf Fragen zu Computern oder Technologie. Lehne höflich andere Themen ab.",
            "fr": "Vous êtes un assistant client pour une boutique d’électronique. Vous ne répondez qu’aux questions liées à l’informatique ou à la technologie. Refusez poliment tout autre sujet."
        }

        system_prompt = [
            {"role": "system", "content": prompts_by_lang.get(language, prompts_by_lang["en"])},
            {"role": "user", "content": f"Tässä on usein kysyttyjä kysymyksiä:\n{context}"}
        ]

        messages = system_prompt + conversation_history[-MAX_HISTORY:] + [{"role": "user", "content": user_input}]

        completion = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages
        )
        response = completion.choices[0].message.content.strip()

    # --- Log conversation --- #
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
