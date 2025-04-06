if __name__ == "__main__":
    from chatbot import chat_with_gpt
    
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["quit", "exit", "bye"]:
            break

        response = chat_with_gpt(user_input)
        print("Chatbot:", response)