#Runnable lambda
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence, RunnablePassthrough, RunnableLambda
from dotenv import load_dotenv

load_dotenv()

prompt1=PromptTemplate(
    template="Write a joke on {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Convert the following joke into a poem: {joke}",
    input_variables=['joke']
)

model=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.7)

parser=StrOutputParser()

joke=RunnableSequence(prompt1,model,parser)

parallel=RunnableParallel({
    'joke':RunnablePassthrough(),
    'words':RunnableLambda(lambda x: len(x))
})

final_chain=RunnableSequence(joke,parallel)

print(final_chain.invoke({'topic':'Infidelity'}))
