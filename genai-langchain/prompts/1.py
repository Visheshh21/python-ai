from pydantic_core.core_schema import NoneSchema
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import streamlit as st
from langchain_core.prompts import PromptTemplate, load_prompt

load_dotenv()

API = os.getenv("GROQ_API_KEY")

st.header("Content Generator")

user_input=st.text_input('Enter your Prompt')

LLM=ChatGroq(api_key=API,
model="openai/gpt-oss-20b",
temperature=0.5,
max_tokens=None)

template=load_prompt("template.json")


if st.button("Generate"):
    chain=template | LLM
    response=chain.invoke({"user_input":user_input})
    st.text(response.content)


