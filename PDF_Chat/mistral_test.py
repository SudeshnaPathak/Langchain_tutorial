import os
from dotenv import load_dotenv
from langchain_community.document_loaders import TextLoader
from langchain_mistralai.chat_models import ChatMistralAI
from langchain_mistralai.embeddings import MistralAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain.chains import create_retrieval_chain

# Load data
load_dotenv()

loader = TextLoader("D:/Langchain_tutorial/Langchain_tutorial/rag/speech.txt")

# Corrected environment variable loading
os.environ["MISTRAL_API_KEY"] = os.getenv("MISTRAL_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

docs = loader.load()

# Split text into chunks 
text_splitter = RecursiveCharacterTextSplitter()
documents = text_splitter.split_documents(docs)

# Define the embedding model
embeddings = MistralAIEmbeddings(model="mistral-embed", mistral_api_key=os.environ["MISTRAL_API_KEY"])

# Create the vector store 
vector = FAISS.from_documents(documents, embeddings)

# Define a retriever interface
retriever = vector.as_retriever()

# Define LLM
model = ChatMistralAI(mistral_api_key=os.environ["MISTRAL_API_KEY"])

# Define prompt template
prompt = ChatPromptTemplate.from_template("""Answer the following question based only on the provided context:

<context>
{context}
</context>

Question: {input}""")

# Create a retrieval chain to answer questions
document_chain = create_stuff_documents_chain(model, prompt)
retrieval_chain = create_retrieval_chain(retriever, document_chain)
response = retrieval_chain.invoke({"input": "Provide a text summary"})
print(response["answer"])
