from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
load_dotenv()



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
         ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\nHere are the tables info : {table_info}\nHere are the tables that you can refer to : {selected_tables}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for reference and should be considered while answering follow up questions.In case of 2 or more tables with same coloumn name ,while displaying the details , if asked for , you should display it from any one of the tables without any ambiguity."),
         few_shot_prompt,
         MessagesPlaceholder(variable_name="messages"),
         ("human", "{input}"),
     ]
      
 )


answer_prompt = PromptTemplate.from_template(
     """Given the following user question, corresponding SQL query, and SQL result, answer the user question to the best of your ability in proper {language}. In case of SQL results , convert it into a dataframe for displaying it to the user and for small answers , answer in a continuous  line.

 Question: {question}
 SQL Query: {query}
 SQL Result: {result}
 Answer: """
 )


