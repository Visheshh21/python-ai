from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.5,
    max_tokens=None
)

while True:
    user_input=input("You: ")
    if user_input== 'exit':
        break
    response=model.invoke(user_input)
    print("AI:",response.content)
