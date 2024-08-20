from typing import List
from fastapi import FastAPI, Request
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
from dotenv import load_dotenv
from langchain.memory import ChatMessageHistory
import os

# Load environment variables
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"] = "true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# Initialize chat history
history = ChatMessageHistory()

# 1. Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to user queries."),
        MessagesPlaceholder(variable_name="messages"),
        ("human", "Question : {question}")
    ]
)

# 2. Create model  
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt | model | parser

# 4. App definition
app = FastAPI(
    title="LangChain Server",
    version="1.0",
    description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route using Langserve
add_routes(app, chain, path="/chain")

# 6. Define a route to handle the interaction (synchronous version)
@app.post("/chain/invoke")
def invoke_chain(request: Request):
    question = request.json().get("input", {}).get("question")
    messages = request.json().get("input", {}).get("messages", [])

    # Update history with past messages
    for message in messages:
        if message["type"] == "human":
            history.add_user_message(message["content"])
        elif message["type"] == "ai":
            history.add_ai_message(message["content"])

    # Invoke chain with updated messages
    response = chain.invoke({"question": question, "messages": history.messages})
    
    # Add the latest interaction to the history
    history.add_user_message(question)
    history.add_ai_message(response)
    
    return {"output": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
