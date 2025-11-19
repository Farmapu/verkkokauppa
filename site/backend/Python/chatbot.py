import os
from datetime import datetime
from dotenv import load_dotenv
from pymongo import MongoClient
from langdetect import detect
from openai import OpenAI

# ------------------------------------------------------
# Environment variables
# ------------------------------------------------------
load_dotenv()

mongo_uri = os.getenv("MONGO_URI")
openai_key = os.getenv("OPENAI_KEY")
if not mongo_uri or not openai_key:
    raise EnvironmentError("Missing MONGO_URI or OPENAI_KEY in .env")

# ------------------------------------------------------
# MongoDB setup
# ------------------------------------------------------
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

# ------------------------------------------------------
# OpenAI setup
# ------------------------------------------------------
openai = OpenAI(api_key=openai_key)

# ------------------------------------------------------
# Chat memory setup
# ------------------------------------------------------
conversation_history = []
last_product_name = None
MAX_HISTORY = 6

SUPPORTED_LANGUAGES = ["fi", "en", "sv", "de", "fr", "es"]

# ------------------------------------------------------
# Utility: Fetch FAQ context
# ------------------------------------------------------
def get_faq_context(limit=30):
    faqs = faq_collection.find({"answer": {"$exists": True}}).limit(limit)
    return "\n".join(f"{faq['question']}: {faq['answer']}" for faq in faqs)

# ------------------------------------------------------
# Utility: Safe product lookup
# ------------------------------------------------------
def find_product_info(product_name):
    """
    Searches all collections for a product by name.
    Prevents None / invalid regex input.
    """
    if not product_name or not isinstance(product_name, str):
        return None

    for col in collections.values():
        product = col.find_one({"name": {"$regex": product_name, "$options": "i"}})
        if product:
            return product

    return None

# ------------------------------------------------------
# Utility: Language-aware formatting
# ------------------------------------------------------
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

# ------------------------------------------------------
# Main chat function
# ------------------------------------------------------
def chat_with_gpt(user_input):
    global last_product_name, conversation_history

    # Detect language from user input
    language = detect(user_input)
    context = get_faq_context()

    # --------------------------------------------------
    # Tech filter – block unrelated topics
    # --------------------------------------------------
    tech_keywords = [
        "cpu", "gpu", "ram", "mobo", "motherboard", "graphics card", "processor",
        "computer", "pc", "ssd", "storage", "cooler", "power supply", "psu",
        "näytönohjain", "prosessori", "muisti", "tietokone", "kovalevy", "emolevy"
    ]

    if not any(word.lower() in user_input.lower() for word in tech_keywords):
        tech_only = {
            "fi": "Voin auttaa vain tietokonekomponentteihin ja teknologiaan liittyvissä kysymyksissä.",
            "en": "I can only help with questions related to computer components or technology.",
            "sv": "Jag kan bara hjälpa till med frågor som rör datorer eller teknik.",
            "es": "Solo puedo ayudarte con preguntas relacionadas con componentes informáticos o tecnología.",
            "de": "Ich kann nur bei Fragen zu Computern oder Technologie helfen.",
            "fr": "Je peux uniquement vous aider avec des questions liées à l’informatique ou à la technologie."
        }
        return tech_only.get(language, tech_only["en"])

    # --------------------------------------------------
    # Try to detect product inside user input
    # --------------------------------------------------
    matched_product = None
    for col in collections.values():
        matched_product = col.find_one({"name": {"$regex": user_input, "$options": "i"}})
        if matched_product:
            last_product_name = matched_product["name"]  # store for later
            break

    # --------------------------------------------------
    # Price/Warranty queries
    # --------------------------------------------------
    price_keywords = ["hinta", "maksaa", "price", "cost", "garanti", "warranty", "takuu"]

    if any(word in user_input.lower() for word in price_keywords):

        # Safe fallback logic
        if matched_product:
            product = matched_product
        elif last_product_name:
            product = find_product_info(last_product_name)
        else:
            product = None

        # If product still not found → ask for clarification
        if not product:
            clarification = {
                "fi": "Voisitko tarkentaa, minkä tuotteen takuusta tai hinnasta haluat tietää?",
                "en": "Could you specify which product you mean?",
            }
            return clarification.get(language, clarification["en"])

        response = format_price_and_warranty(product, language)

    # --------------------------------------------------
    # "Show all" collection queries
    # --------------------------------------------------
    elif any(cmd in user_input.lower() for cmd in ["show all rams", "näytä kaikki muistit"]):
        all_rams = list(collections["ram"].find())
        if not all_rams:
            return "RAM-muisteja ei löytynyt tietokannasta."
        response = "\n".join(
            f"Nimi: {r.get('name')}, Hinta: {r.get('Price', {}).get('totalPrice')} €, Takuu: {r.get('Warranty')} v"
            for r in all_rams
        )

    elif any(cmd in user_input.lower() for cmd in ["show all cpus", "näytä kaikki prosessorit"]):
        all_cpus = list(collections["cpu"].find())
        if not all_cpus:
            return "Prosessoreita ei löytynyt."
        response = "\n".join(
            f"Nimi: {c.get('name')}, Hinta: {c.get('Price', {}).get('totalPrice')} €, Takuu: {c.get('Warranty')} v"
            for c in all_cpus
        )

    elif any(cmd in user_input.lower() for cmd in ["show all gpus", "näytä kaikki näytönohjaimet"]):
        all_gpus = list(collections["gpu"].find())
        if not all_gpus:
            return "Näytönohjaimia ei löytynyt."
        response = "\n".join(
            f"Nimi: {g.get('name')}, Hinta: {g.get('Price', {}).get('totalPrice')} €, Takuu: {g.get('Warranty')} v"
            for g in all_gpus
        )

    elif any(cmd in user_input.lower() for cmd in ["show all mobos", "näytä kaikki emolevyt", "show all motherboards"]):
        all_mobos = list(collections["mobo"].find())
        if not all_mobos:
            return "Emolevyjä ei löytynyt."
        response = "\n".join(
            f"Nimi: {m.get('name')}, Hinta: {m.get('Price', {}).get('totalPrice')} €, Takuu: {m.get('Warranty')} v"
            for m in all_mobos
        )

    # --------------------------------------------------
    # Default GPT response
    # --------------------------------------------------
    else:
        prompts_by_lang = {
            "en": "You are a polite assistant for an online electronics store. Only answer questions related to computer hardware or technology.",
            "fi": "Olet ystävällinen asiakaspalvelurobotti, joka auttaa vain tietokonekomponentteihin ja teknologiaan liittyvissä asioissa.",
            "sv": "Du hjälper endast med datorrelaterade frågor.",
            "es": "Solo respondes preguntas sobre hardware o tecnología.",
            "de": "Du beantwortest nur Fragen zur Computerhardware.",
            "fr": "Vous répondez uniquement aux questions liées à la technologie."
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

    # --------------------------------------------------
    # Save conversation to memory + DB log
    # --------------------------------------------------
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
