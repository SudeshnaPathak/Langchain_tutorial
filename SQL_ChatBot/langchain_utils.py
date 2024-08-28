import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from table_details import table_chain 
from prompts import final_prompt, answer_prompt
import datetime

load_dotenv()

db_user = os.getenv("db_user")
db_password = os.getenv("db_password")
db_host = os.getenv("db_host")
db_name = os.getenv("db_name")
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")
context = db.get_context()
table_info = context["table_info"]


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)

def get_chain():
    print("Creating chain")
    generate_query = create_sql_query_chain(llm, db,final_prompt) 
    execute_query = QuerySQLDataBaseTool(db=db)
    rephrase_answer = answer_prompt | llm | StrOutputParser()
    chain = (
    RunnablePassthrough.assign(selected_tables=table_chain) |
    RunnablePassthrough.assign(query=generate_query).assign(
        result= itemgetter("query") | execute_query
        ) 
        | rephrase_answer
    )

    return chain
# | rephrase_answer in place of | StrOutputParser()

if __name__ == "__main__":
    chain = get_chain()
    while True:
        question = input("Enter a Question: ")
        start_time = datetime.datetime.now()
        response = chain.invoke({"question": question , "messages" : []})
        print(str(response['result']))
        print("Time Taken: " , datetime.datetime.now() - start_time) 