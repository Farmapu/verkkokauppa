import sys
from chatbot import chat_with_gpt

print(chat_with_gpt(sys.argv[1]))

sys.stdout.flush()