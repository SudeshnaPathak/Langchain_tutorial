# -- import necessary libraries --
from typing import List
import datetime
from fastapi import FastAPI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables import RunnablePassthrough
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_openai import ChatOpenAI
from langserve import add_routes
import os
from operator import itemgetter
from dotenv import load_dotenv
from langchain_utils import get_chain
from langchain_core.pydantic_v1 import BaseModel, Field

load_dotenv()

# +++++++++++++++++ Constant values from env ++++++++++++++++++++++++

# -- Langsmith tracking --
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")

# -- OpenAI API --
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# +++++++++++++++++ Model Structure Creation +++++++++++++++++++++++

# -- Chat Model --
model = ChatOpenAI(model="gpt-3.5-turbo-0125")

# -- Define the session history storage --
store = {}

# -- Define the session history getter --
def get_session_history(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store:
    store[session_id] = InMemoryChatMessageHistory()
  return store[session_id]

# -- Define the chat history trimmer --
trimmer = trim_messages(
    max_tokens=1000,
    strategy="last",
    token_counter=model,
    include_system=True,
    allow_partial=False,
    start_on="human",
)


sql_chain = get_chain()
# -- Create chain --
# chain = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | prompt | model | parser
chain = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer )| sql_chain

# -- Create the chain with history --
chain_with_history = RunnableWithMessageHistory(
    chain,
    get_session_history,
    input_messages_key="messages",
)



# if __name__=="__main__":
#     while True:
#       Query = input("Query: ")
#       Language = input("Langauge: ")
#       SessionId = input("Session ID: ")
#       start_time = datetime.datetime.now()
#       print("\n")

#       response = chain_with_history.invoke(
#         {"messages": [HumanMessage(content=Query)], 
#          "language": Language , 
#          "question": Query},
#         config={"configurable": {"session_id": SessionId}},
#       )

#       print("Response: " + response)
#       print("Time Taken: " , datetime.datetime.now() - start_time)
#       print("\n")



class QueryRequest(BaseModel):
    question: str
    language: str
    sessionid: str

app = FastAPI()

@app.post("/api/v1/query")
async def get_response(request: QueryRequest):
  print("\n======================================\n")

  # Extract the query from the request body
  Question = request.question
  Language = request.language
  SessionId = request.sessionid

  print("Question   : " + str(Question))
  print("Language   : " + str(Language))
  print("Session ID : " + str(SessionId))
  print("\n")

  response = chain_with_history.invoke(
      {
        "messages": [HumanMessage(content=Question)],
        "language": Language,
        "question": Question
      },
      config={"configurable": {"session_id": SessionId}},
    )
  
  print("Response: " + str(response))
  
  return {"response": response}



if __name__ == "__main__":
  import multiprocessing
  import subprocess
  import uvicorn

  # workers = multiprocessing.cpu_count() * 2 + 1

  uvicorn_cmd = [
      "uvicorn",
      "main:app",
      # "--host=localhost",
      "--port=8080",
      # f"--workers={workers}",
      "--reload"
  ]

  # uvicorn.run(app, host="0.0.0.0", port=8000, reload=True, workers=workers)
  subprocess.run(uvicorn_cmd)