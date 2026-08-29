from torch._dynamo.utils import enum_repr
from langchain_huggingface import HuggingFaceEmbeddings
from dotenv import load_dotenv
from sklearn.metrics.pairwise import cosine_similarity
import numpy as numpy

load_dotenv()

embedding=HuggingFaceEmbeddings(model_name="BAAI/bge-m3")

documents=['Virat Kohli is an Indian cricketer known for his aggressive batting and leadership.' ,
"MS Dhoni is a former Indian captain famous for his calm demeanor and finishing skills.",
"Sachin Tendulkar, also known as the 'God of Cricket',holds many batting records. " ,
"Rohit Sharma is known for his elegant batting and record-breaking double centuries. ",
"Jasprit Bumrah is an Indian fast bowler known for his unorthodox action and yorkers. "]

embed=embedding.embed_documents(documents)

query="tell me about Indian Captain"

query_embedding=embedding.embed_query(query)

similarity=cosine_similarity([query_embedding],embed)[0]

index,score=sorted(list(enumerate(similarity)),key=lambda x:x[1],reverse=True)[0]
print(documents[index],score)