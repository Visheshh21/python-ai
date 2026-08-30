from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from langchain_classic.output_parsers import StructuredOutputParser, ResponseSchema
from dotenv import load_dotenv

load_dotenv()

model = ChatGroq(model_name="openai/gpt-oss-20b", temperature=0.5, max_tokens=None)

Schema = [
    ResponseSchema(name='fact1', description='first fact about the topic'),
    ResponseSchema(name='fact2', description='second fact about the topic'),
    ResponseSchema(name='fact3', description='third fact about the topic')
]

parser = StructuredOutputParser.from_response_schemas(Schema)

template = PromptTemplate(
    template="Give 3 facts about the {topic} \n {format_instructions}",
    input_variables=['topic'],
    partial_variables={'format_instructions': parser.get_format_instructions()}
)

chain = template | model | parser 

result = chain.invoke({'topic': 'the mentalist'})
print(result)