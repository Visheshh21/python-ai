#Runnable Parallel
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel, RunnableSequence
from dotenv import load_dotenv

load_dotenv()

prompt1=PromptTemplate(
    template="Generate a Linkedin Post about {topic}",
    input_variables=['topic']
)

prompt2=PromptTemplate(
    template="Generate 5 tweet for the topic {topic}",
    input_variables=['topic']
)

prompt3=PromptTemplate(
    template="Merge the linkedin post and tweets into a single document \n Linkedin Post:{linkedin}\n Tweets:{tweets}",
    input_variables=['linkedin','tweets']
)

model1=ChatGroq(model_name="openai/gpt-oss-20b",temperature=0.7)

parser=StrOutputParser()

parallel=RunnableParallel({
    'linkedin':RunnableSequence(prompt1,model1,parser),
    'tweets':RunnableSequence(prompt2,model1,parser)
})
print(parallel.invoke({'topic':'Disobidience in Finances'}))
final_chain=RunnableSequence(parallel,prompt3,model1,parser)

print(final_chain.invoke({'topic':'Stoicism in my veins'}))