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
        ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\nHere are the tables info : {table_info}\nHere are the tables that you can refer to : {selected_tables}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for reference and should be considered while answering follow up questions. In case of 2 or more tables with same coloumn name, while displaying the details, if asked for, you should display it from any one of the tables without any ambiguity. Answer only from the Database and not from anywhere else. Include all the column names and table names within backticks while generating the SQL queries for correct execution. For string matching, always use the format similar to: WHERE `Column_Name` LIKE 'Value%'. Generate SQL queries as plain text without using triple backticks or markdown formatting."),
        few_shot_prompt,
        MessagesPlaceholder(variable_name="messages"),
        ("human", "{input}"),
    ]  
 )

question_prompt = ChatPromptTemplate.from_template(""" You are an expert assistant in reframing questions. If the user's question specifically asks for a report, reframe the question to include the following details: the detailed NOC Guidelines, definitions of some technical terms related to groundwater, and generalized Training Opportunities related to Groundwater.

If the user asks for anything other than a report, return the user's original question without modification. Do not rephrase or generate a new question in this case.

Question: {question}""")

# question_prompt = ChatPromptTemplate.from_template(""" You are an assisstant expert in reframing Questions. If the user asks to generate a report in his question,
#                                             then modify the question to provide the NOC Guidelines, definition of some technical terms related to groundwater, generalised Training Opportunities related to Groundwater.
#                                             Include the use in the question if mentioned in the user's question, otherwise omit the section and add the extra portion in the question, other than the report if it is provided in the user's question.
#                                             If the user is not asking to generate a Report then return the given question. Do not generate a new question or concatetenate anything to the question in this case.                               
    
# Question: {question}""")


answer_prompt = PromptTemplate.from_template(
     """Given the following user question, corresponding 'SQL Query', and 'SQL Result', answer the user question to the best of your ability in proper {language}. In case of 'SQL Result' with multiple rows convert it into a tabular format for displaying it to the user and for small answers, answer in a continuous line. If you don't know the answer just say "NA" only.  
     

 Question: {question}
 SQL Query: {query}
 SQL Result: {result}
 Always print the 'SQL Query' even if it is NA
 Answer: """
 )

sql_prompt = PromptTemplate.from_template(
        """Return the input question exactly as it is as the answer.
        
    Question: {query}
    Answer: """
)

