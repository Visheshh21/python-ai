#RAG= Document Loaders + Text Splitters + Vector Databases + Retrievers
#TextLoaders
from langchain_community.document_loaders import TextLoader
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

LLM=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.7)
parser=StrOutputParser()
prompt1=PromptTemplate(
    template="Summarize the following text in 50 words: {text}",
    input_variables=['text']
)

loader=TextLoader('1.txt',encoding='utf-8')
docs=loader.load()

chain=RunnableSequence(prompt1,LLM,parser)
print(chain.invoke(docs[0].page_content))