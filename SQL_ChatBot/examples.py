from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# examples = [
#     {
#   "input": "Find the total number of orders placed by customers in the USA.",
#   "query": "SELECT COUNT(*) FROM orders o JOIN customers c ON o.customerNumber = c.customerNumber WHERE c.country = 'USA';"
# },
# {
#   "input": "Retrieve the names and cities of all employees who work in the 'EMEA' territory.",
#   "query": "SELECT firstName, lastName, city FROM employees e JOIN offices o ON e.officeCode = o.officeCode WHERE o.territory = 'EMEA';"
# },
# {
#   "input": "List all products that have more than 1000 units in stock.",
#   "query": "SELECT productName FROM products WHERE quantityInStock > 1000;"
# },
# {
#   "input": "Get the details of the order with the highest total amount.",
#   "query": "SELECT o.orderNumber, SUM(od.quantityOrdered * od.priceEach) AS totalAmount FROM orders o JOIN orderdetails od ON o.orderNumber = od.orderNumber GROUP BY o.orderNumber ORDER BY totalAmount DESC LIMIT 1;"
# },
# {
#   "input": "Find the average credit limit of customers in Germany.",
#   "query": "SELECT AVG(creditLimit) FROM customers WHERE country = 'Germany';"
# },
# {
#   "input": "List all orders that were shipped after the required date.",
#   "query": "SELECT * FROM orders WHERE shippedDate > requiredDate;"
# },
# {
#   "input": "Show the product names and their respective vendors for all products in the 'Planes' product line.",
#   "query": "SELECT productName, productVendor FROM products WHERE productLine = 'Planes';"
# },
# {
#   "input": "Get the number of employees who report to the employee with employee number 1002.",
#   "query": "SELECT COUNT(*) FROM employees WHERE reportsTo = 1002;"
# },
# {
#   "input": "Retrieve the details of all payments made before January 1, 2023.",
#   "query": "SELECT * FROM payments WHERE paymentDate < '2023-01-01';"
# }

# ]


examples= [
        {
            "input": "Give me the groundwater depth and aquifer details for all wells in a specific village.",
            "query": "SELECT Village, Well_ID, Well_Depth (meters), Aquifer FROM ground_water_level-2015-2022 WHERE Village = 'Village_X' ORDER BY Well_ID;"
        },
        {
            "input": "Provide the pre-monsoon and post-monsoon groundwater levels for all years in a specific village.",
            "query": "SELECT Village, Well_ID, Pre-monsoon_2015 (meters below ground level), Post-monsoon_2015 (meters below ground level), Pre-monsoon_2016 (meters below ground level), Post-monsoon_2016 (meters below ground level), Pre-monsoon_2017 (meters below ground level), Post-monsoon_2017 (meters below ground level), Pre-monsoon_2018 (meters below ground level), Post-monsoon_2018 (meters below ground level), Pre-monsoon_2019 (meters below ground level), Post-monsoon_2019 (meters below ground level), Pre-monsoon_2020 (meters below ground level), Post-monsoon_2020 (meters below ground level), Pre-monsoon_2021 (meters below ground level), Post-monsoon_2021 (meters below ground level), Pre-monsoon_2022 (meters below ground level), Post-monsoon_2022 (meters below ground level) FROM ground_water_level-2015-2022 WHERE Village = 'Village_X' ORDER BY Well_ID;"
        },
        {
            "input": "Retrieve the water contamination levels for a specific state.",
            "query": "SELECT State_Name, pH, TDS, Turbidity, Chloride, Total_Alkalinity, Total_Hardness, Sulphate, Iron, Total_Arsenic, Fluoride, Nitrate, Residual_Chlorine, E_coli, Total_Coliform FROM villagecontamination WHERE State_Name = 'State_X' ORDER BY SNo;"
        },
        {
            "input": "Give me the list of all contaminated sources in a specific state.",
            "query": "SELECT State_Name, S_No, Sources_Found_Contaminated FROM water_quality_testing WHERE State_Name = 'State_X' AND Sources_Found_Contaminated > 0 ORDER BY S_No;"
        },
        {
            "input": "List the wells with the deepest groundwater levels in a specific state.",
            "query": "SELECT Well_ID, State_Name, Well_Depth (meters) FROM ground_water_level-2015-2022 WHERE State_Name = 'State_X' ORDER BY Well_Depth (meters) DESC;"
        },
        {
            "input": "Compare water quality parameters for all monitoring locations in a specific state.",
            "query": "SELECT Name of Monitoring Location, pH, Conductivity (μmhos/cm), BOD (mg/L), Nitrate N (mg/L), Fluoride (mg/L), Arsenic (mg/L) FROM water_quality_data_ground_water WHERE State_Name = 'State_X' ORDER BY Name of Monitoring Location;"
        },
        {
            "input": "Identify villages with the highest levels of a specific contaminant in a state.",
            "query": "SELECT Village, State_Name, Fluoride, Total_Arsenic FROM villagecontamination WHERE State_Name = 'State_X' AND (Fluoride > 1.5 OR Total_Arsenic > 0.01) ORDER BY Village;"
        },
        {
            "input": "Provide details of remedial measures taken in contaminated areas of a specific state.",
            "query": "SELECT State_Name, S_No, Remedial_Measures_Taken FROM water_quality_testing WHERE State_Name = 'State_X' AND Remedial_Measures_Taken > 0 ORDER BY S_No;"
        },
        {
            "input": "Retrieve the water quality testing status for a specific state.",
            "query": "SELECT State_Name, Total_Sources, Sources_Tested, Sources_Yet_To_Be_Tested, Sources_Found_Safe, Sources_Found_Contaminated FROM water_quality_testing WHERE State_Name = 'State_X';"
        },
        {
            "input": "Find monitoring locations with the highest BOD levels in a specific state.",
            "query": "SELECT Name of Monitoring Location, BOD (mg/L) FROM water_quality_data_ground_water WHERE State_Name = 'State_X' ORDER BY BOD (mg/L) DESC;"
        }
    ]



def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)
    return example_selector



