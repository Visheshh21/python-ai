from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

#chat template
chat_template=ChatPromptTemplate([
    ('system','You are a helpful customer service agent'),
    MessagesPlaceholder(variable_name='chat_history'),
    ('human','{question}')
])

chat_history=[]
#load chat history
with open('chat_history.txt') as f:
    chat_history.extend(f.readlines())

print(chat_history)
#create prompt

prompt=chat_template.invoke({'chat_history':chat_history,'question':"Where is my order"})

print(prompt)