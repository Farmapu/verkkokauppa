from chatbot import chat_with_gpt

print("AI: Hei! Miten voin olla avuksi?")

while True:
    user_input = input("I: ")
    if user_input.lower() in ["lopeta", "poistu", "exit", "quit"]:
        break

    response = chat_with_gpt(user_input)
    print("AI:", response)