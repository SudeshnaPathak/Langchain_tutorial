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
from prompts import final_prompt, answer_prompt, sql_prompt
from sql_connection import sql_cursor , format_results_as_list , format_results_as_markdown
from langchain_core.runnables import RunnableLambda
import datetime
import traceback
from langchain_core.messages.ai import AIMessage

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
model = os.getenv("model")

# llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
# llm = ChatOpenAI(model="gpt-4-turbo", temperature=0)
llm = ChatOpenAI(model=model, temperature=0)

def execute_sql_query(response):
    response = response['response']
    response_query_list = response.split("\n\n")
    cursor = sql_cursor()
    table_list = []
    try:
     
        for i , query in enumerate(response_query_list):
            query = query.replace(';' , '')
            query = query.replace('\n' , ' ')
            print(query)
            cursor.execute(query)
            myresponse = list(cursor.fetchall())
            headers = [i[0].replace('_',' ') for i in cursor.description]
            print(headers)
            table = format_results_as_markdown(headers , myresponse)
            # df = pd.DataFrame(table)
            # df = df.apply(lambda x: x.str.replace('\n', '', regex=False) if x.dtype == "object" else x)
            # print(df.to_csv(f"output/output{i}.csv",index = False , header = False , sep = '|'))
            # table_list.append(df.to_csv(index = False , header = False , sep = '|')) 
            print(table)
               
    except:
        print(traceback.format_exc())
        return AIMessage(content="NA")
    
    return AIMessage(content=table)
    

def get_chain():
    print("Creating chain")
    generate_query = create_sql_query_chain(llm, db, final_prompt)
    # exact_chain = sql_prompt | llm | StrOutputParser()
    # execute_query = QuerySQLDataBaseTool(db=db , verbose = True)
    # rephrase_answer = answer_prompt | llm | StrOutputParser()
    # chain = (
    # RunnablePassthrough.assign(selected_tables=table_chain) |
    # RunnablePassthrough.assign(query=generate_query).assign(
    #     result= itemgetter("query") | execute_query
    #     ) 
    #     | rephrase_answer
    # )

    chain = (
        RunnablePassthrough.assign(selected_tables=table_chain) |
        RunnablePassthrough.assign(query=generate_query).assign(
        response=itemgetter("query")) | execute_sql_query | StrOutputParser()
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