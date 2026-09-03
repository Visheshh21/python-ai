from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain_core.runnables import RunnableBranch, RunnableLambda
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from pydantic import BaseModel, Field
from typing import Literal


load_dotenv()

class Feedback(BaseModel):
    sentiment: Literal['Positive','Negative']=Field(description='the sentiment of the feedback')
    feedback: str=Field(description='the feedback text')

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

parser1=StrOutputParser()

parser=PydanticOutputParser(pydantic_object=Feedback)

prompt1=PromptTemplate(
    template="Classify the sentiment for the following feedback text into positive or negative \n {text} \n {format_instructions}",
    input_variables=['text'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
)

classifier_chain=prompt1 | model | parser

result1=classifier_chain.invoke({'text':'this is a wonderful product and i hate it'})

print(result1)

prompt2=PromptTemplate(
    template="Write an appropriate response to this positive feedback \n {feedback}",
    input_variables=['feedback']
)

prompt3=PromptTemplate(
    template="Write an appropriate response to this negative feedback \n {feedback}",
    input_variables=['feedback']
)


branch=RunnableBranch(
    (lambda x:x.sentiment=='Positive', prompt2 | model | parser1),
    (lambda x:x.sentiment=="Negative", prompt3 | model | parser1),
    RunnableLambda(lambda x:"could not find sentiment")
)

final_chain=classifier_chain | branch

result2=final_chain.invoke({'text':'this is a wonderful product and i hate it'})

print(result2)