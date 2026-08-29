from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_groq import ChatGroq
from dotenv import load_dotenv

load_dotenv()

model=ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0.5,
    max_tokens=None
)

messages=[
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="Tell me about BAAI/bge-m3")   
]

result=model.invoke(messages)

messages.append(AIMessage(content=result.content))

print(messages)