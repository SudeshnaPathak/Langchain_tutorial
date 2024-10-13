import pandas as pd
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from langchain.chains.openai_tools import create_extraction_chain_pydantic
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from operator import itemgetter
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

model = os.getenv("model")
llm = ChatOpenAI(model=model, temperature=0)

def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details

class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")


table_details = get_table_details()

system = f"""Return the names of ALL the SQL tables that MIGHT be relevant to the user question. \
The tables details are:

{table_details}

Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed."""

final_table_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", system),
        ("human", "{input}"),
         MessagesPlaceholder(variable_name="messages")
    ]
)

table_details_prompt = f"""Given the following SQL tables:

{table_details}

Return the names of ALL the SQL tables that MIGHT be relevant to the user's question. 
Remember to include ALL POTENTIALLY RELEVANT tables, even if you're not sure that they're needed.
User's question: "{input}"

"""


# llm_with_tools = llm.bind_tools([Table])
# output_parser = PydanticToolsParser(tools=[Table])
# table_select_chain = final_table_prompt | llm_with_tools | output_parser

table_select_chain = create_extraction_chain_pydantic(Table, llm, system_message=table_details_prompt)

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    table_names = {}
    table_names["tables"] = tables
    return table_names

table_chain = {"input": itemgetter("question")} | table_select_chain| get_tables

