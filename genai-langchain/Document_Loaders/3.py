from langchain_community.document_loaders import WebBaseLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()

url='https://jalammar.github.io/illustrated-transformer/'
loader=WebBaseLoader(url)
docs=loader.load()

LLM=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.7)
prompt1=PromptTemplate(
    template="what is the core idea of the following text: {text}",
    input_variables=['text']
)

parser=StrOutputParser()
chain=RunnableSequence(prompt1,LLM,parser)

for doc in docs:
    print(chain.invoke(doc.page_content))