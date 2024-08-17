import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
import time

# Load environment variables
load_dotenv()
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")
os.environ['MISTRAL_API_KEY'] = os.getenv("MISTRAL_API_KEY")

# Function to extract text from PDFs
def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

# Function to split text into chunks
def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000, chunk_overlap=1000)
    chunks = text_splitter.split_text(text)
    return chunks

# Function to create a vector store from text chunks
def get_vector_store(text_chunks):
    embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=os.environ['MISTRAL_API_KEY'])
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index_mistral")
    return vector_store

# Function to create the conversational chain
def get_conversational_chain():
    prompt_template = """
    Answer the following question based only on the provided context:

    <context>
    {context}
    </context>

    Question: {input}
    """
# model = "mistral-large-latest" 
    llm = ChatMistralAI(model = "mistral-large-latest" , mistral_api_key=os.environ['MISTRAL_API_KEY'])
    prompt = ChatPromptTemplate.from_template(template=prompt_template)
    chain = load_qa_chain(llm, chain_type="stuff", prompt=prompt)
    return chain

# Function to handle user input and display the response
def user_input(user_question):
    start_time = time.time()   
    new_db = st.session_state.get("vector_store")
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain(
        {"input_documents": docs, "input": user_question},
        return_only_outputs=True
    )
    
    st.write("Reply: ", response["output_text"])
    st.write("Time taken: ", time.time() - start_time)

# Main function for the Streamlit app
def main():
    st.set_page_config(page_title="Chat with multiple PDFs")
    st.header("Chat with multiple PDFs using MISTRAL💁")

    user_question = st.text_input("Ask a Question from the PDF Files")

    if user_question:
        user_input(user_question)

    with st.sidebar:
        st.title("Menu:")
        pdf_docs = st.file_uploader("Upload your PDF Files and Click on the Submit & Process Button", accept_multiple_files=True)
        if st.button("Submit & Process"):
            with st.spinner("Processing..."):
                start_time = time.time()
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vector_store = get_vector_store(text_chunks)
                st.session_state.vector_store = vector_store
                st.success(f"Done \n Time Taken: {time.time() - start_time}" )

if __name__ == "__main__":
    main()

