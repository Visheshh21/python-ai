from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser


load_dotenv()

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

parser=StrOutputParser()

prompt1=PromptTemplate(
    template="Classify the sentiment for the following feedback text into positive or negative \n {text}",
    input_variables=['text']
)

classifier_chain=prompt1 | model | parser

result=classifier_chain.invoke({'text':'this is a terrible product and i hate it'})

print(result)