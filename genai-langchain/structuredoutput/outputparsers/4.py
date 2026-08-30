from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import PydanticOutputParser
from pydantic import BaseModel,Field
from dotenv import load_dotenv

load_dotenv()

class Student(BaseModel):
    name: str=Field(default='Vishesh',description="name of the student")
    age: int=Field(default=21,description='age of the student')
    
parser=PydanticOutputParser(pydantic_object=Student)

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

template=PromptTemplate(
    template='Generate the name and age of the finctional {place} person \n {format_instructions}',
    input_variables=['place'],
    partial_variables={'format_instructions':parser.get_format_instructions()}
    )

chain=template | model | parser

result=chain.invoke({'place':'Turkey'})

chain.get_graph().print_ascii()

print(result)
