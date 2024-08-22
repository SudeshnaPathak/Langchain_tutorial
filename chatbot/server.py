#!/usr/bin/env python
from typing import List, Union

from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate,MessagesPlaceholder
from langchain.schema import SystemMessage, HumanMessage, AIMessage
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os
from dotenv import load_dotenv 
load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
#Langsmith tracking
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# 1. Create prompt template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system" , "You are a helpful assistant.Please respond to user queries."),
         MessagesPlaceholder(variable_name="messages"),
        ("human" , "Question : {question}")
    ]
)

# 2. Create model
model = ChatOpenAI()

# 3. Create parser
parser = StrOutputParser()

# 4. Create chain
chain = prompt | model | parser

class InputChat(BaseModel):
    """Input for the chat endpoint."""

    messages: List[Union[HumanMessage, AIMessage, SystemMessage]] = Field(
        ...,
        description="The chat messages representing the current conversation.",
    )

# 4. App definition
app = FastAPI(
  title="LangChain Server",
  version="1.0",
  description="A simple API server using LangChain's Runnable interfaces",
)

# 5. Adding chain route

add_routes(
    app,
    chain.with_types(input_type=InputChat),
    path="/chain",
    enable_feedback_endpoint=True,
    enable_public_trace_link_endpoint=True,
    playground_type='chat'
)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)