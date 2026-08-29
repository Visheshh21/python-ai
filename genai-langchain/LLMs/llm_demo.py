from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

API = os.getenv("GROQ_API_KEY")

LLM=ChatGroq(api_key=API,
model="openai/gpt-oss-20b",
temperature=0.5,
max_tokens=500)
response=LLM.invoke("tell me something about BC and AD. why do they exist")
print(response.content)

