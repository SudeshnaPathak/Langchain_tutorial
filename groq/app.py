import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.embeddings import OllamaEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain
from langchain_community.vectorstores import FAISS
from dotenv import load_dotenv 
import time

load_dotenv()
# Load the groq API key
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if "vector" not in st.session_state:
    st.session_state.embeddings=OllamaEmbeddings()
    st.session_state.loader=WebBaseLoader("https://docs.smith.langchain.com/")
    st.session_state.docs = st.session_state.loader.load()
    st.session_state.text_splitter = RecursiveCharacterTextSplitter(chunk_size = 1000 , chunk_overlap = 200)
    st.session_state.final_documents = st.session_state.text_splitter.split_documents(st.session_state.docs[:1])
    st.session_state.vector = FAISS.from_documents(st.session_state.final_documents,st.session_state.embeddings)

st.title("ChatGroq Demo")
llm = ChatGroq(groq_api_key = GROQ_API_KEY ,
               model = " mixtral-8x7b-32768")
prompt = ChatPromptTemplate.from_template(
    """
    Answer the questions based on the provided context only.
    Please provide the most accurate response based on the questiom
    <context>
    {context}
    <context>
    Questions : {input}
"""
)

document_chain = create_stuff_documents_chain(llm , prompt)
retriever = st.session_state.vector.as_retriever()
retrieval_chain = create_retrieval_chain(retriever , document_chain)

prompt = st.text_input("Input your prompt here")
if prompt:
    start = time.process_time()
    response = retrieval_chain.invoke({"input" :prompt})
    print("Response time :" , time.process_time() - start)
    st.write(response['answer'])
    
    #with a streamlit expander
    with st.expander("Document Similarity Search"):
        #Find relevant chunks
        for i , doc in enumerate(response["context"]):
            st.write(doc.page_content)
            st.write("----------------------------------------")
