from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()

chat_template=ChatPromptTemplate([
    ('system','"You are a helpful {role}"'),
    ('human','what is {user_input}')
])

prompt=chat_template.invoke({'role':'comedian','user_input':'tell me a joke'})

print(prompt)