from chatbot import chat_with_gpt

print("Bot: Hei! Miten voin olla avuksi?")

while True:
    user_input = input("Sinä: ")
    if user_input.lower() in ["lopeta", "poistu", "exit", "quit"]:
        print("Bot: Kiitos. Kysy vain jos tarvitset lisää apua. Hei hei!")
        break

    response = chat_with_gpt(user_input)
    print("Bot:", response)