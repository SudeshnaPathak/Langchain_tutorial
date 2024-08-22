import pandas as pd
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.pydantic_v1 import BaseModel, Field
from prompts import table_final_prompt
from langchain_openai import ChatOpenAI
from operator import itemgetter
from typing import List


llm = ChatOpenAI(model="gpt-3.5-turbo-0125", temperature=0)
def get_table_details():
    # Read the CSV file into a DataFrame
    table_description = pd.read_csv("classicmodels_table_descriptions.csv")
    table_docs = []

    # Iterate over the DataFrame rows to create Document objects
    table_details = ""
    for index, row in table_description.iterrows():
        table_details = table_details + "Table Name:" + row['Table'] + "\n" + "Table Description:" + row['Description'] + "\n\n"

    return table_details

class Table(BaseModel):
    """Table in SQL database."""

    name: str = Field(description="Name of table in SQL database.")



final_table_prompt = table_final_prompt
llm_with_tools = llm.bind_tools([Table])
output_parser = PydanticToolsParser(tools=[Table])

table_select_chain = final_table_prompt | llm_with_tools | output_parser

def get_tables(tables: List[Table]) -> List[str]:
    tables  = [table.name for table in tables]
    table_names = {}
    table_names["tables"] = tables
    return table_names

table_chain = {"input": itemgetter("question")} | table_select_chain| get_tables