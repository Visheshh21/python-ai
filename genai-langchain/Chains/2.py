from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv
from langchain_core.runnables import RunnableParallel

load_dotenv()

model1=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)
model2=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)
model3=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.5,max_tokens=None)

parser=StrOutputParser()

prompt1=PromptTemplate(
    template="Generate short and simple notes on {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Generate 5 short question answers from the topic {topic}",
    input_variables=['topic']
)

prompt3=PromptTemplate(
    template="Merge the provided notes and quiz into a single document \n Notes:{notes}\n Quiz:{quiz}",
    input_variables=['notes','quiz']
)

parallel_chain=RunnableParallel({
    'notes': prompt1 | model1 | parser,
    'quiz': prompt2 | model2 | parser
})

merge_chain=prompt3|model3|parser

final_chain=parallel_chain|merge_chain

result=final_chain.invoke({'topic':'procastination'})

print(result)