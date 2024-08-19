import os
from dotenv import load_dotenv
from langchain_community.utilities.sql_database import SQLDatabase
from langchain.chains import create_sql_query_chain
from langchain_openai import ChatOpenAI
from langchain_community.tools.sql_database.tool import QuerySQLDataBaseTool
from operator import itemgetter
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.pydantic_v1 import BaseModel, Field
from typing import List
from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import OpenAIEmbeddings
from operator import itemgetter

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough


import pandas as pd
from langchain.memory import ChatMessageHistory
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["LANGCHAIN_TRACING_V2"]="true"
os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGCHAIN_API_KEY")


db_user = "root"
db_password = "root"
db_host = "localhost"  
db_port = "3306"  
db_name = "classicmodels"
db = SQLDatabase.from_uri(f"mysql+pymysql://{db_user}:{db_password}@{db_host}/{db_name}")


llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
generate_query = create_sql_query_chain(llm , db)


execute_query_tool = QuerySQLDataBaseTool(db = db)

def few_shot_prompt_generate_template(question):
        examples = [
        {
    "input": "Find the total number of orders placed by customers in the USA.",
    "query": "SELECT COUNT(*) FROM orders o JOIN customers c ON o.customerNumber = c.customerNumber WHERE c.country = 'USA';"
    },
    {
    "input": "Retrieve the names and cities of all employees who work in the 'EMEA' territory.",
    "query": "SELECT firstName, lastName, city FROM employees e JOIN offices o ON e.officeCode = o.officeCode WHERE o.territory = 'EMEA';"
    },
    {
    "input": "List all products that have more than 1000 units in stock.",
    "query": "SELECT productName FROM products WHERE quantityInStock > 1000;"
    },
    {
    "input": "Get the details of the order with the highest total amount.",
    "query": "SELECT o.orderNumber, SUM(od.quantityOrdered * od.priceEach) AS totalAmount FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY o.orderNumber ORDER BY totalAmount DESC LIMIT 1;"
    },
    {
    "input": "Find the average credit limit of customers in Germany.",
    "query": "SELECT AVG(creditLimit) FROM customers WHERE country = 'Germany';"
    },
    {
    "input": "List all orders that were shipped after the required date.",
    "query": "SELECT * FROM orders WHERE shippedDate > requiredDate;"
    },
    {
    "input": "Show the product names and their respective vendors for all products in the 'Planes' product line.",
    "query": "SELECT productName, productVendor FROM products WHERE productLine = 'Planes';"
    },
    {
    "input": "Get the number of employees who report to the employee with employee number 1002.",
    "query": "SELECT COUNT(*) FROM employees WHERE reportsTo = 1002;"
    },
    {
    "input": "Retrieve the details of all payments made before January 1, 2023.",
    "query": "SELECT * FROM payments WHERE paymentDate < '2023-01-01';"
    }

    ]

        
        example_selector = SemanticSimilarityExampleSelector.from_examples(
            examples,
            OpenAIEmbeddings(),
            FAISS,
            k=5,
            input_keys=["input"],
        )

        example_selector.select_examples({"input": question}) 

        from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
        example_prompt = ChatPromptTemplate.from_messages(
                [
                    ("human", "{input}\nSQLQuery:"),
                    ("ai", "{query}"),
                ]
            )
        few_shot_prompt = FewShotChatMessagePromptTemplate(
                example_prompt=example_prompt,
                example_selector=example_selector,
                input_variables=["input","top_k"],
            )
        few_shot_prompt.format(input=question)
        # print(few_shot_prompt.format(input=question))
        # print(type(few_shot_prompt))
    
        
context = db.get_context()



def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("classicmodels_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"
    return table_details
   
table_details = get_table_details()

class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables details are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{input}"),
    ]
)
llm_with_tools = llm.bind_tools([Table])
output_parser = PydanticToolsParser(tools=[Table])

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    table_names = {}
    table_names["tables"] = tables
    return table_names

table_chain = {"input": itemgetter("question")} | prompt | llm_with_tools | output_parser| get_tables

history = ChatMessageHistory()

final_prompt = ChatPromptTemplate.from_messages(
     [
         ("system", "You are a MySQL expert. Given an input question, create a syntactically correct MySQL query to run. Unless otherwise specificed.\nHere are the tables info : {table_info}\nHere are the tables that you can refer to : {selected_tables}\n\nBelow are a number of examples of questions and their corresponding SQL queries. Those examples are just for reference and should be considered while answering follow up questions"),
         few_shot_prompt,
         MessagesPlaceholder(variable_name="messages"),
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

rephrase_answer = answer_prompt | llm | StrOutputParser()


chain =(RunnablePassthrough.assign(selected_tables=table_chain)|
       RunnablePassthrough.assign(query=generate_query).assign(
        result=itemgetter("query") | execute_query_tool)) | rephrase_answer


def get_response(question):
    few_shot_prompt_generate_template(question)
    response = chain.invoke({"question": question,"messages":history.messages})
    history.add_user_message(question)
    history.add_ai_message(response)
    return response