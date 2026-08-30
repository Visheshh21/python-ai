from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import JsonOutputParser
from dotenv import load_dotenv

load_dotenv()

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

parser=JsonOutputParser()

template=PromptTemplate(
    template='Give me the name, age and city of a fictional person \n {format_instruction}',
    input_variables=[],
    partial_variables={'format_instruction':parser.get_format_instructions()}
)


chain=template | model | parser

result=chain.invoke({})

print(result)
