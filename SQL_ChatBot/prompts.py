from examples import get_example_selector
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder,FewShotChatMessagePromptTemplate,PromptTemplate
from table_details import get_table_details
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


table_details = get_table_details()

system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables details are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

table_final_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{input}"),
    ]
)