from langchain_groq import ChatGroq
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage

load_dotenv()

model=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.5,
    max_tokens=500
)

chat_history=[
    SystemMessage(content="You are a helpful Assistant")
]

while True:
    user_input=input("You: ")
    if user_input== 'exit':
        break
    chat_history.append(HumanMessage(content=user_input))
    response=model.invoke(chat_history)
    print("AI:",response.content)
    chat_history.append(AIMessage(content=response.content))

print(chat_history)