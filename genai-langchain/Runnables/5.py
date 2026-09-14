#Runnable Branch
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnablePassthrough, RunnableLambda, RunnableBranch
from dotenv import load_dotenv

load_dotenv()

prompt1=PromptTemplate(
    template="Write a report on {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Limit this to 100 words: {report}",
    input_variables=['report']
)


model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.7)

parser=StrOutputParser()

report_gen=RunnableSequence(prompt1,model,parser)

branch=RunnableBranch(
    (lambda x:len(x.split())>200, RunnableSequence(prompt2,model,parser)),
    RunnablePassthrough()
)

result=RunnableSequence(report_gen,branch)

print(result.invoke({'topic':'how do we limit ourselves to our own incapabilites, rather than being jealous'}))