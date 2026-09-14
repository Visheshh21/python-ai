#Sequential Runnable
#R1-prompt, R2-LLM

from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableSequence
from dotenv import load_dotenv

load_dotenv()
LLM=ChatGroq(model_name='openai/gpt-oss-20b', temperature=0.5, max_tokens=None)
prompt1=PromptTemplate(
    template="Write a joke about {topic}",
    input_variables=['topic']
)

parser=StrOutputParser()

prompt2=PromptTemplate(
    template="Convert the following joke into a poem: {joke}",
    input_variables=['joke']
)
chain=RunnableSequence(prompt1,LLM,parser,prompt2,LLM,parser)

print(chain.invoke('Python'))