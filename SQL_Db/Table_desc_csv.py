import csv

# Define the table details
tables = [
    {
        "Table": "productlines",
        "Description": "Contains information about various product lines, including text descriptions, HTML formatted descriptions, and images. Each product line categorizes a group of products and is identified by a unique product line code."
    },
    {
        "Table": "products",
        "Description": "Stores details of individual products offered by the company. Each product is associated with a product line, has a unique product code, and includes attributes such as name, scale, vendor, description, quantity in stock, buying price, and Manufacturer's Suggested Retail Price (MSRP)."
    },
    {
        "Table": "offices",
        "Description": "Contains information about the company's offices, including office codes, location details (city, state, country), contact numbers, and address details. Each office is uniquely identified by an office code."
    },
    {
        "Table": "employees",
        "Description": "Stores data about employees, including their employee numbers, names, job titles, contact information, and office codes. It also includes a self-referencing foreign key 'reportsTo' that identifies the employee's manager."
    },
    {
        "Table": "customers",
        "Description": "Holds customer information, including names, contact details, addresses, and associated sales representatives (referenced by employee number). It also tracks the customer's credit limit, which is used for financial operations."
    },
    {
        "Table": "payments",
        "Description": "Records payments made by customers, capturing the customer number, payment date, payment amount, and check number. Each payment entry is linked to a specific customer."
    },
    {
        "Table": "orders",
        "Description": "Documents customer orders, including the order date, required delivery date, shipping date, status, and any comments. Each order is associated with a specific customer, and the orders are uniquely identified by an order number."
    },
    {
        "Table": "orderdetails",
        "Description": "Contains details of the products ordered, including the order number, product code, quantity ordered, price per item, and the order line number. This table links specific products to their respective orders."
    }
]


# Specify the file name
filename = 'classicmodels_table_descriptions.csv'

# Write the data to a CSV file
with open(filename, mode='w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=["Table", "Description"])
    writer.writeheader()  # Write the header row
    writer.writerows(tables)  # Write the table details

print(f"CSV file '{filename}' created and saved successfully.")
