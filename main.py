from chatbot import chat_with_gpt
if __name__ == "__main__":
    print("Chatbot is ready! type in quit, if you want to exit")
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)