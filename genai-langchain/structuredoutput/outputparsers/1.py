from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

output_parser=StrOutputParser()

prompt1=PromptTemplate(template="""
Tell me about this concept in 100 words {concept}
""",input_variables=["concept"])

prompt2=PromptTemplate(template="""
What are some related concepts to this {output}
""",input_variables=["output"])

chain = prompt1 | model | output_parser | prompt2 | model | output_parser

result=chain.invoke({"concept":"quantum computing"})

print(result)
