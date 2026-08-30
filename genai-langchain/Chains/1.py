from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

prompt1=PromptTemplate(
    template="""
    Generate a detailed report on {concept}
    """,
    input_variables=["concept"]
)

prompt2=PromptTemplate(
    template="""
    Give me 5 key points from this {report}
    """,
    input_variables=["report"]
)

parser=StrOutputParser()

chain = prompt1 | model | parser | prompt2 | model | parser

result = chain.invoke({"concept":"python"})

print(result)