from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
load_dotenv()

# db_user = os.getenv("db_user")
# db_password = os.getenv("db_password")
# db_host = os.getenv("db_host")
# db_name = os.getenv("db_name")
# db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


example_prompt = ChatPromptTemplate.from_messages(
     [
         ("human", "{input}\nSQLQuery:"),
         ("ai", "{query}"),
     ]
 )


few_shot_prompt = FewShotChatMessagePromptTemplate(
     example_prompt=example_prompt,
     example_selector=get_example_selector(),
     input_variables=["input","top_k"],
 )


final_prompt = ChatPromptTemplate.from_messages(
     [
         ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\nHere are the tables info : {table_info}\nHere are the tables that you can refer to : {selected_tables}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for reference and should be considered while answering follow up questions"),
         few_shot_prompt,
         ("human", "{input}"),
     ]
      
 )


answer_prompt = PromptTemplate.from_template(
     """Given the following user question, corresponding SQL query, and SQL result, answer the user question.

 Question: {question}
 SQL Query: {query}
 SQL Result: {result}
 Answer: """
 )


