# -- import necessary libraries --
from typing import List, Any
import datetime
import pandas as pd
from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from async_generator import async_generator , yield_
from typing import AsyncGenerator
import asyncio
from langchain.callbacks.streaming_aiter import AsyncIteratorCallbackHandler
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_core.messages import HumanMessage, AIMessage, trim_messages
from langchain_core.chat_history import BaseChatMessageHistory, InMemoryChatMessageHistory
from langchain_core.runnables import RunnablePassthrough , RunnableParallel
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.schema import LLMResult
from langchain_openai import ChatOpenAI
import os
from operator import itemgetter
from dotenv import load_dotenv
from langchain_utils import get_chain
from text_utils import text_chain
from langchain_core.pydantic_v1 import BaseModel, Field
from Modular_function import newloggingfunction
from sql_connection import sql_cursor , format_results_as_list



load_dotenv()

print = newloggingfunction("JalShakti", str(datetime.datetime.now().strftime("%Y%m%d")))

# +++++++++++++++++ Constant values from env ++++++++++++++++++++++++

# -- Langsmith tracking --
os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGCHAIN_TRACING_V2")
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


# +++++++++++++++++ Model Structure Creation +++++++++++++++++++++++

# -- Chat Model --
model = ChatOpenAI(model="gpt-3.5-turbo-0125")

# -- Define the session history storage --
store_sql = {}
store_text = {}

# -- Define the session history getter --
def get_session_history_sql(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store_sql:
    store_sql[session_id] = InMemoryChatMessageHistory()
  return store_sql[session_id]

def get_session_history_text(session_id: str) -> BaseChatMessageHistory:
  if session_id not in store_text:
    store_text[session_id] = InMemoryChatMessageHistory()
  return store_text[session_id]

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
text_chain = text_chain

# -- Create chain --
# chain = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer) | prompt | model | parser
chain1 = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer )| sql_chain 
chain2 = RunnablePassthrough.assign(messages=itemgetter("messages") | trimmer )| text_chain 
# map_chain = RunnableParallel(text=chain2, sql=chain1)

# -- Create the chain with history --
chain_with_history_sql = RunnableWithMessageHistory(
    chain1,
    get_session_history_sql,
    input_messages_key="messages",
)

chain_with_history_text = RunnableWithMessageHistory(
    chain2,
    get_session_history_text,
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
#       print("Response: ")
#       print(response)
#       print("Time Taken: " , datetime.datetime.now() - start_time)
#       print("\n")



class QueryRequest(BaseModel):
    question: str
    language: str
    sessionid: str

app = FastAPI()

# @app.post("/api/v1/sql_stream")
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
    
    # Define a generator function that yields the streaming response
    async def stream_response() -> AsyncGenerator[str, None]:
        async for token in chain_with_history_sql.astream(
            {
                "messages": [HumanMessage(content=Question)],
                "language": Language,
                "question": Question
            },
            config={"configurable": {"session_id": SessionId}},
        ):
            yield token
            await asyncio.sleep(0)
            print(token)

    # Return the streaming response
    return StreamingResponse(stream_response(), media_type="text/plain")

# @app.post("/api/v1/text_stream")
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
    
    # Define a generator function that yields the streaming response
    async def stream_response() -> AsyncGenerator[str, None]:
        async for token in chain_with_history_text.astream(
            {
                "messages": [HumanMessage(content=Question)],
                "language": Language,
                "question": Question
            },
            config={"configurable": {"session_id": SessionId}},
        ):
            yield token
            await asyncio.sleep(0)
            print(token)

    # Return the streaming response
    return StreamingResponse(stream_response(), media_type="text/plain")

# Modify the get_response function to support streaming
# @app.post("/api/v1/query")
# async def get_response(request: QueryRequest):
#     print("\n======================================\n")

#     # Extract the query from the request body
#     Question = request.question
#     Language = request.language
#     SessionId = request.sessionid

#     print("Question   : " + str(Question))
#     print("Language   : " + str(Language))
#     print("Session ID : " + str(SessionId))
#     print("\n")

#     # Function to generate response stream
#     @async_generator
#     async def response_generator():
#         for r in chain_with_history.stream(
#         {
#           "messages": [HumanMessage(content=Question)],
#           "language": Language,
#           "question": Question
#         },
#         config={"configurable": {"session_id": SessionId}},
#         ):
            
#             await yield_(r)
#             await asyncio.sleep(0.1)
#             print(r)  # Simulate processing time or slow down for streaming

#     return StreamingResponse(response_generator(), media_type="text/event-stream") #text/event-stream



# @app.post("/api/v1/query")
# async def get_response(request: QueryRequest):
#   print("\n======================================\n")

#   # Extract the query from the request body
#   Question = request.question
#   Language = request.language
#   SessionId = request.sessionid

#   response = ""

#   print("Question   : " + str(Question))
#   print("Language   : " + str(Language))
#   print("Session ID : " + str(SessionId))
#   print("\n")

#   for r in chain_with_history.stream(
#       {
#         "messages": [HumanMessage(content=Question)],
#         "language": Language,
#         "question": Question
#       },
#       config={"configurable": {"session_id": SessionId}},
#     ):

#     response = response + r
  
#     print("Response: " + str(response))
  
#     yield {"response": response}



# @app.post("/api/v1/sql")
# async def get_response(request: QueryRequest):
#   print("\n======================================\n")

#   # Extract the query from the request body
#   Question = request.question
#   Language = request.language
#   SessionId = request.sessionid

#   print("Question   : " + str(Question))
#   print("Language   : " + str(Language))
#   print("Session ID : " + str(SessionId))
#   print("\n")

#   response = chain_with_history_sql.invoke(
#       {
#         "messages": [HumanMessage(content=Question)],
#         "language": Language,
#         "question": Question
#       },
#       config={"configurable": {"session_id": SessionId}},
#     )
  
#   print("Response: " + str(response))
#   return response
# #   return {"response": f"{response['text']} \n {response['sql']}"}

@app.post("/api/v1/sql")
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

  response = chain_with_history_sql.invoke(
      {
        "messages": [HumanMessage(content=Question)],
        "language": Language,
        "question": Question
      },
      config={"configurable": {"session_id": SessionId}},
    )
  
  print("Response: " + str(response))
  response_query_list = response['query'].split("\n\n")
  cursor = sql_cursor()
  table_list = []
  
  for i , query in enumerate(response_query_list):
        query = query.replace(';' , '')
        cursor.execute(query)
        myresponse = list(cursor.fetchall())
        headers = [i[0] for i in cursor.description]
        print(headers)
        table = format_results_as_list(headers , myresponse)
        df = pd.DataFrame(table)
        df = df.apply(lambda x: x.str.replace('\n', '', regex=False) if x.dtype == "object" else x)
        print(df.to_csv(f"output/output{i}.csv",index = False , header = False , sep = '|'))
        table_list.append(df.to_csv(index = False , header = False , sep = '|'))    
  
  
  return {"response" : table_list}
  

@app.post("/api/v1/text")
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

  response = chain_with_history_text.invoke(
      {
        "messages": [HumanMessage(content=Question)],
        "language": Language,
        "question": Question
      },
      config={"configurable": {"session_id": SessionId}},
    )
  
  print("Response: " + str(response))
  return {"response" : response}

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