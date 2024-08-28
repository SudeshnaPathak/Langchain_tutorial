import streamlit as st
from PyPDF2 import PdfReader
from langchain.text_splitter import RecursiveCharacterTextSplitter
import os
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv
from langchain.chains.question_answering import load_qa_chain
import time



load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=10000 , chunk_overlap =1000)
    chunks = text_splitter.split_text(text)
    return chunks

def get_vector_store(text_chunks):
    embeddings = OpenAIEmbeddings()
    vector_store = FAISS.from_texts(text_chunks , embedding = embeddings)
    vector_store.save_local("jalshakti_faiss_index")
    

def get_conversational_chain():
     prompt_template = """
    Answer the question as detailed as possible from the provided context, make sure to provide all the details, if the answer is not in
    provided context just say, "answer is not available in the context", don't provide the wrong answer\n\n
    Context:\n {context}?\n
    Question: \n{question}\n

    Answer:
    """
     llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
     prompt = PromptTemplate(template = prompt_template , input_variables={"context","question"})
     chain = load_qa_chain(llm , chain_type="stuff" , prompt=prompt)
     return chain

def user_input(user_question):
    start_time = time.time()
    embeddings = OpenAIEmbeddings()
    
    new_db = FAISS.load_local("jalshakti_faiss_index", embeddings,allow_dangerous_deserialization=True)
    docs = new_db.similarity_search(user_question)

    chain = get_conversational_chain()

    response = chain.invoke(
        {"input_documents":docs, "question": user_question}
        , return_only_outputs=True)
    
    
    print(response)
    

def main():
    print("Chat with multiple PDFs using Gemini💁")

    pdf_folder_path = input("Enter the folder path containing your PDF files: ")
    
    if os.path.exists(pdf_folder_path):
        pdf_docs = [os.path.join(pdf_folder_path, f) for f in os.listdir(pdf_folder_path) if f.endswith('.pdf')]
        print("Processing...") 
        raw_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(raw_text)
        get_vector_store(text_chunks)
        print("Done")
    else:
        print("The specified folder path does not exist.")

    while True:
        user_question = input("Ask a Question from the PDF Files: ")

        if user_question:
            user_input(user_question)


if __name__ == "__main__":
    main()
