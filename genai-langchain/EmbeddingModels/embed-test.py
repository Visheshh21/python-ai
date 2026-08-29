from langchain_huggingface import HuggingFaceEmbeddings

embedding1 = HuggingFaceEmbeddings(model_name='BAAI/bge-m3')
text="Delhi is the capital of India"
vector1=embedding1.embed_query(text)
print(str(vector1))
