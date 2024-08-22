from langchain_community.vectorstores import FAISS
from langchain_core.example_selectors import SemanticSimilarityExampleSelector
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
import os

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

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

def get_example_selector():
    example_selector = SemanticSimilarityExampleSelector.from_examples(
    examples,
    OpenAIEmbeddings(),
    FAISS,
    k=5,
    input_keys=["input"],
)
    return example_selector



