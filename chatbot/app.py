from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import os
from dotenv import load_dotenv
# import sys
# sys.path.append(os.path.dirname(__file__))
import streamlit as st
load_dotenv()


os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

##Prompt Template 
prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful assistant.Please respond to user queries."),
        ("user" , "Question : {question}")
    ]
)

## streamlit framework
st.title("Langchain Demo with OpenAI API")
input_text = st.text_input("Search the topic you want")

# openAI llm
llm = ChatOpenAI(model = "gpt-3.5-turbo")
output_parser = StrOutputParser()
chain = prompt|llm|output_parser

if input_text :
    st.write(chain.invoke({'question' : input_text}))


