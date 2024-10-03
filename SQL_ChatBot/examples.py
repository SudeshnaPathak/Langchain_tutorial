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


# examples = [
#     {
#         "input": "Give me the groundwater depth and aquifer details for all wells in a specific village.",
#         "query": "SELECT `Village`, `Well_ID`, `Well_Depth(meters)`, `Aquifer` FROM `ground_water_level_2015_to_2022` WHERE `Village` = 'Village_X' ORDER BY `Well_ID`;"
#     },
#     {
#         "input": "Provide the pre-monsoon and post-monsoon groundwater levels for all years in a specific village.",
#         "query": "SELECT `Village`, `Well_ID`, `Pre-monsoon_2015(meters below ground level)`, `Post-monsoon_2015(meters below ground level)`, `Pre-monsoon_2016(meters below ground level)`, `Post-monsoon_2016(meters below ground level)`, `Pre-monsoon_2017(meters below ground level)`, `Post-monsoon_2017(meters below ground level)`, `Pre-monsoon_2018(meters below ground level)`, `Post-monsoon_2018(meters below ground level)`, `Pre-monsoon_2019(meters below ground level)`, `Post-monsoon_2019(meters below ground level)`, `Pre-monsoon_2020(meters below ground level)`, `Post-monsoon_2020(meters below ground level)`, `Pre-monsoon_2021(meters below ground level)`, `Post-monsoon_2021(meters below ground level)`, `Pre-monsoon_2022(meters below ground level)`, `Post-monsoon_2022(meters below ground level)` FROM `ground_water_level_2015_to_2022` WHERE `Village` = 'Village_X' ORDER BY `Well_ID`;"
#     },
#     {
#         "input": "Retrieve the water contamination levels for a specific state.",
#         "query": "SELECT `State_Name`, `pH`, `TDS`, `Turbidity`, `Chloride`, `Total_Alkalinity`, `Total_Hardness`, `Sulphate`, `Iron`, `Total_Arsenic`, `Fluoride`, `Nitrate`, `Residual_Chlorine`, `E_coli`, `Total_Coliform` FROM `village_water_contamination` WHERE `State_Name` = 'State_X' ORDER BY `SNo`;"
#     },
#     {
#         "input": "Give me the list of all contaminated sources in a specific state.",
#         "query": "SELECT `State_Name`, `S_No`, `Sources_Found_Contaminated` FROM `ground_water_quality_testing` WHERE `State_Name` = 'State_X' AND `Sources_Found_Contaminated` > 0 ORDER BY `S_No`;"
#     },
#     {
#         "input": "List the wells with the deepest groundwater levels in a specific state.",
#         "query": "SELECT `Well_ID`, `State_Name`, `Well_Depth(meters)` FROM `ground_water_level_2015_to_2022` WHERE `State_Name` = 'State_X' ORDER BY `Well_Depth(meters)` DESC;"
#     },
#     {
#         "input": "Compare water quality parameters for all monitoring locations in a specific state.",
#         "query": "SELECT `Name of Monitoring Location`, `pH_Max`, `pH_Min`, `Conductivity_Max(μmhos/cm)`, `Conductivity_Min(μmhos/cm)`, `BOD_Max(mg/L)`, `BOD_Min(mg/L)`, `Nitrate_N_Max(mg/L)`, `Nitrate_N_Min(mg/L)`, `Fluoride_Max(mg/L)`, `Fluoride_Min(mg/L)`, `Arsenic_Max(mg/L)`, `Arsenic_Min(mg/L)` FROM `ground_water_quality_data` WHERE `State_Name` = 'State_X' ORDER BY `Name of Monitoring Location`;"
#     },
#     {
#         "input": "Identify villages with the highest levels of a specific contaminant in a state.",
#         "query": "SELECT `Village`, `State_Name`, `Fluoride`, `Total_Arsenic` FROM `village_water_contamination` WHERE `State_Name` = 'State_X' AND (`Fluoride` > 1.5 OR `Total_Arsenic` > 0.01) ORDER BY `Village`;"
#     },
#     {
#         "input": "Provide details of remedial measures taken in contaminated areas of a specific state.",
#         "query": "SELECT `State_Name`, `S_No`, `Remedial_Measures_Taken` FROM `ground_water_quality_testing` WHERE `State_Name` = 'State_X' AND `Remedial_Measures_Taken` > 0 ORDER BY `S_No`;"
#     },
#     {
#         "input": "Retrieve the water quality testing status for a specific state.",
#         "query": "SELECT `State_Name`, `Total_Sources`, `Sources_Tested`, `Sources_Yet_To_Be_Tested`, `Sources_Found_Safe`, `Sources_Found_Contaminated` FROM `ground_water_quality_testing` WHERE `State_Name` = 'State_X';"
#     },
#     {
#         "input": "Find monitoring locations with the highest BOD levels in a specific state.",
#         "query": "SELECT `Name of Monitoring Location`, `BOD_Max(mg/L)` FROM `ground_water_quality_data` WHERE `State_Name` = 'State_X' ORDER BY `BOD_Max(mg/L)` DESC;"
#     },
#     # {
#     #     "input": "Which states have the highest stage of groundwater development and are classified as over-exploited?",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Stage of Goundwater Development (%)`, `Classification`
#     #     FROM `ground_water_resources_data`
#     #     WHERE `Classification` = 'Over-Exploited'
#     #     ORDER BY `Stage of Goundwater Development (%)` DESC;
#     #     """
#     # },
#     # {
#     #     "input": "Identify districts where the volume available for artificial recharge structures is less than the water required for recharge.",
#     #     "query": """
#     #     SELECT `State`, `Disctrict`, `Available Sub-surface Volume for ARS (MCM)`, `Water Required for Recharge (MCM)`
#     #     FROM `artificial_recharge_structure_data`
#     #     WHERE `Available Sub-surface Volume for ARS (MCM)` < `Water Required for Recharge (MCM)`;
#     #     """
#     # },
#     # {
#     #     "input": "Find the annual groundwater draft (total) for districts where the projected demand for domestic and industrial use by 2025 exceeds 100 MCM.",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Annual Groundwater Draft(Total)`, `Projected Demand for Domestic & Industrial Use Upto 2025`
#     #     FROM `ground_water_resources_data`
#     #     WHERE `Projected Demand for Domestic & Industrial Use Upto 2025` > 100;
#     #     """
#     # },
#     # {
#     #     "input": "List the states where groundwater contamination with arsenic exceeds 0.01 mg/L.",
#     #     "query": """
#     #     SELECT `State_Name`, `Name_of_Monitoring_Location`, `Arsenic_Max (mg/L)`
#     #     FROM `ground_water_quality_data`
#     #     WHERE CAST(`Arsenic_Max (mg/L)` AS DECIMAL(10,3)) > 0.01;
#     #     """
#     # },
#     # {
#     #     "input": "Retrieve districts with a significant difference in pre-monsoon and post-monsoon water levels in 2021 (more than 5 meters).",
#     #     "query": """
#     #     SELECT `State_Name`, `District_Name`, `Block_Name`, 
#     #            `Pre-monsoon_2021 (meters below ground level)`, 
#     #            `Post-monsoon_2021 (meters below ground level)`, 
#     #            ABS(`Pre-monsoon_2021 (meters below ground level)` - `Post-monsoon_2021 (meters below ground level)`) AS `Difference`
#     #     FROM `ground_water_level_2015_2022`
#     #     WHERE ABS(`Pre-monsoon_2021 (meters below ground level)` - `Post-monsoon_2021 (meters below ground level)`) > 5;
#     #     """
#     # },
#     # {
#     #     "input": "How many water sources have been tested and found safe across all states?",
#     #     "query": """
#     #     SELECT `State_Name`, SUM(`Sources_Tested`) AS `Total_Sources_Tested`, SUM(`Sources_Found_Safe`) AS `Safe_Sources`
#     #     FROM `ground_water_quality_testing`
#     #     GROUP BY `State_Name`;
#     #     """
#     # },
#     # {
#     #     "input": "What is the total geographical area identified for artificial recharge structures across states, and which state has the largest identified area?",
#     #     "query": """
#     #     SELECT `State`, SUM(`Area Identified for ARS (Sq. Km.)`) AS `Total Area Identified`
#     #     FROM `artificial_recharge_structure_data`
#     #     GROUP BY `State`
#     #     ORDER BY `Total Area Identified` DESC
#     #     LIMIT 1;
#     #     """
#     # },
#     # {
#     #     "input": "Identify states where total dissolved solids (TDS) exceed 1000 mg/L in both minimum and maximum values.",
#     #     "query": """
#     #     SELECT `State_Name`, `Name_of_Monitoring_Location`, `Total Dissolved Solids_Min (mg/L)`, `Total Dissolved Solids_Max (mg/L)`
#     #     FROM `ground_water_quality_data`
#     #     WHERE CAST(`Total Dissolved Solids_Min (mg/L)` AS DECIMAL(10,2)) > 1000
#     #       AND CAST(`Total Dissolved Solids_Max (mg/L)` AS DECIMAL(10,2)) > 1000;
#     #     """
#     # },
#     # {
#     #     "input": "List districts where natural discharge during the non-monsoon season is more than 20% of annual replenishable groundwater resources.",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Natural Discharge During Non-Monsoon Season`, `Annual Replenishable Groundwater Resources (Total)`, 
#     #            (`Natural Discharge During Non-Monsoon Season` / `Annual Replenishable Groundwater Resources (Total)`) * 100 AS `Discharge Percentage`
#     #     FROM `ground_water_resources_data`
#     #     WHERE (`Natural Discharge During Non-Monsoon Season` / `Annual Replenishable Groundwater Resources (Total)`) * 100 > 20;
#     #     """
#     # },
#     # {
#     #     "input": "Determine the average pre-monsoon groundwater level for 2020 across all districts.",
#     #     "query": """
#     #     SELECT AVG(`Pre-monsoon_2020 (meters below ground level)`) AS `Average Pre-Monsoon Level 2020`
#     #     FROM `ground_water_level_2015_2022`;
#     #     """
#     # },
#     # {
#     #     "input": "Identify states where the groundwater availability for future irrigation use is less than 50% of the net groundwater availability.",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Net Groundwater Availability`, `Groundwater Availability for Future Irrigation Use`,
#     #            (`Groundwater Availability for Future Irrigation Use` / `Net Groundwater Availability`) * 100 AS `Percentage for Irrigation Use`
#     #     FROM `ground_water_resources_data`
#     #     WHERE (`Groundwater Availability for Future Irrigation Use` / `Net Groundwater Availability`) * 100 < 50;
#     #     """
#     # },
#     # {
#     #     "input": "List all districts where the volume available for artificial recharge structures is more than the volume of the unsaturated zone.",
#     #     "query": """
#     #     SELECT `State`, `Disctrict`, `Volume for Unsaturated Zone (MCM)`, `Available Sub-surface Volume for ARS (MCM)`
#     #     FROM `artificial_recharge_structure_data`
#     #     WHERE `Available Sub-surface Volume for ARS (MCM)` > `Volume for Unsaturated Zone (MCM)`;
#     #     """
#     # },
#     # {
#     #     "input": "Find districts where the stage of groundwater development is more than 100% and the total dissolved solids exceed 2000 mg/L.",
#     #     "query": """
#     #     SELECT r.`State Name`, r.`District Name`, r.`Stage of Goundwater Development (%)`, q.`Total Dissolved Solids_Max (mg/L)`
#     #     FROM `ground_water_resources_data` r
#     #     JOIN `ground_water_quality_data` q ON r.`District Name` = q.`State_Name`
#     #     WHERE r.`Stage of Goundwater Development (%)` > 100
#     #     AND CAST(q.`Total Dissolved Solids_Max (mg/L)` AS DECIMAL(10,2)) > 2000;
#     #     """
#     # },
#     # {
#     #     "input": "Identify blocks where pre-monsoon levels from 2015 to 2020 show a consistent decline year after year.",
#     #     "query": """
#     #     SELECT `State_Name`, `District_Name`, `Block_Name`
#     #     FROM `ground_water_level_2015_2022`
#     #     WHERE `Pre-monsoon_2015 (meters below ground level)` < `Pre-monsoon_2016 (meters below ground level)`
#     #     AND `Pre-monsoon_2016 (meters below ground level)` < `Pre-monsoon_2017 (meters below ground level)`
#     #     AND `Pre-monsoon_2017 (meters below ground level)` < `Pre-monsoon_2018 (meters below ground level)`
#     #     AND `Pre-monsoon_2018 (meters below ground level)` < `Pre-monsoon_2019 (meters below ground level)`
#     #     AND `Pre-monsoon_2019 (meters below ground level)` < `Pre-monsoon_2020 (meters below ground level)`;
#     #     """
#     # },
#     # {
#     #     "input": "Which states have both high fluoride and arsenic contamination (fluoride > 1.5 mg/L and arsenic > 0.01 mg/L)?",
#     #     "query": """
#     #     SELECT `State_Name`, `Name_of_Monitoring_Location`, `Fluoride_Max (mg/L)`, `Arsenic_Max (mg/L)`
#     #     FROM `ground_water_quality_data`
#     #     WHERE CAST(`Fluoride_Max (mg/L)` AS DECIMAL(10,2)) > 1.5
#     #     AND CAST(`Arsenic_Max (mg/L)` AS DECIMAL(10,3)) > 0.01;
#     #     """
#     # },
#     # {
#     #     "input": "For each state, find the total annual groundwater draft and total available groundwater resources, then calculate the percentage usage of available resources.",
#     #     "query": """
#     #     SELECT `State Name`, 
#     #            SUM(`Annual Groundwater Draft(Total)`) AS `Total Groundwater Draft`,
#     #            SUM(`Annual Replenishable Groundwater Resources (Total)`) AS `Total Groundwater Resources`,
#     #            (SUM(`Annual Groundwater Draft(Total)`) / SUM(`Annual Replenishable Groundwater Resources (Total)`)) * 100 AS `Usage Percentage`
#     #     FROM `ground_water_resources_data`
#     #     GROUP BY `State Name`;
#     #     """
#     # },
#     # {
#     #     "input": "Identify districts with high nitrate contamination, where nitrate levels exceed 45 mg/L and the sources are found contaminated during testing.",
#     #     "query": """
#     #     SELECT q.`State_Name`, q.`Name_of_Monitoring_Location`, q.`Nitrate N_Max (mg/L)`, t.`Sources_Found_Contaminated`
#     #     FROM `ground_water_quality_data` q
#     #     JOIN `ground_water_quality_testing` t ON q.`State_Name` = t.`State_Name`
#     #     WHERE CAST(q.`Nitrate N_Max (mg/L)` AS DECIMAL(10,2)) > 45
#     #     AND t.`Sources_Found_Contaminated` > 0;
#     #     """
#     # },
#     # {
#     #     "input": "Retrieve the districts where the annual domestic and industrial draft is more than 50% of the total groundwater draft.",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Annaul Domestic and Industry Draft`, `Annual Groundwater Draft(Total)`,
#     #            (`Annaul Domestic and Industry Draft` / `Annual Groundwater Draft(Total)`) * 100 AS `Domestic & Industry Percentage`
#     #     FROM `ground_water_resources_data`
#     #     WHERE (`Annaul Domestic and Industry Draft` / `Annual Groundwater Draft(Total)`) * 100 > 50;
#     #     """
#     # },
#     # {
#     #     "input": "Find states where the well depth is more than 100 meters and the pre-monsoon groundwater level is consistently below 50 meters from 2015 to 2020.",
#     #     "query": """
#     #     SELECT `State_Name`, `District_Name`, `Well_Depth (meters)`, `Pre-monsoon_2015 (meters below ground level)`, 
#     #            `Pre-monsoon_2016 (meters below ground level)`, `Pre-monsoon_2017 (meters below ground level)`, 
#     #            `Pre-monsoon_2018 (meters below ground level)`, `Pre-monsoon_2019 (meters below ground level)`, 
#     #            `Pre-monsoon_2020 (meters below ground level)`
#     #     FROM `ground_water_level_2015_2022`
#     #     WHERE `Well_Depth (meters)` > 100
#     #     AND `Pre-monsoon_2015 (meters below ground level)` > 50
#     #     AND `Pre-monsoon_2016 (meters below ground level)` > 50
#     #     AND `Pre-monsoon_2017 (meters below ground level)` > 50
#     #     AND `Pre-monsoon_2018 (meters below ground level)` > 50
#     #     AND `Pre-monsoon_2019 (meters below ground level)` > 50
#     #     AND `Pre-monsoon_2020 (meters below ground level)` > 50;
#     #     """
#     # },
#     # {
#     #     "input": "Find districts where the percentage of groundwater availability for future irrigation is more than 50%, and the demand for domestic and industrial use in 2025 is expected to be less than 50 MCM.",
#     #     "query": """
#     #     SELECT `State Name`, `District Name`, `Groundwater Availability for Future Irrigation Use`, `Net Groundwater Availability`, 
#     #            `Projected Demand for Domestic & Industrial Use Upto 2025`,
#     #            (`Groundwater Availability for Future Irrigation Use` / `Net Groundwater Availability`) * 100 AS `Future Irrigation Percentage`
#     #     FROM `ground_water_resources_data`
#     #     WHERE (`Groundwater Availability for Future Irrigation Use` / `Net Groundwater Availability`) * 100 > 50
#     #     AND `Projected Demand for Domestic & Industrial Use Upto 2025` < 50;
#     #     """
#     # }
# ]

examples = [
    {
        "input": "Give me the groundwater depth and aquifer details for all wells in a specific village.",
        "query": "SELECT `Village`, `Well_ID`, `Well_Depth(meters)`, `Aquifer` FROM `ground_water_level_2015_to_2022` WHERE `Village` LIKE 'Village_X%' ORDER BY `Well_ID`;"
    },
    {
        "input": "Provide the pre-monsoon and post-monsoon groundwater levels for all years in a specific village.",
        "query": "SELECT `Village`, `Well_ID`, `Pre-monsoon_2015(meters below ground level)`, `Post-monsoon_2015(meters below ground level)`, `Pre-monsoon_2016(meters below ground level)`, `Post-monsoon_2016(meters below ground level)`, `Pre-monsoon_2017(meters below ground level)`, `Post-monsoon_2017(meters below ground level)`, `Pre-monsoon_2018(meters below ground level)`, `Post-monsoon_2018(meters below ground level)`, `Pre-monsoon_2019(meters below ground level)`, `Post-monsoon_2019(meters below ground level)`, `Pre-monsoon_2020(meters below ground level)`, `Post-monsoon_2020(meters below ground level)`, `Pre-monsoon_2021(meters below ground level)`, `Post-monsoon_2021(meters below ground level)`, `Pre-monsoon_2022(meters below ground level)`, `Post-monsoon_2022(meters below ground level)` FROM `ground_water_level_2015_to_2022` WHERE `Village` LIKE 'Village_X%' ORDER BY `Well_ID`;"
    },
    {
        "input": "Retrieve the water contamination levels for a specific state.",
        "query": "SELECT `State_Name`, `pH`, `TDS`, `Turbidity`, `Chloride`, `Total_Alkalinity`, `Total_Hardness`, `Sulphate`, `Iron`, `Total_Arsenic`, `Fluoride`, `Nitrate`, `Residual_Chlorine`, `E_coli`, `Total_Coliform` FROM `village_water_contamination` WHERE `State_Name` LIKE 'State_X%' ORDER BY `SNo`;"
    },
    {
        "input": "Give me the list of all contaminated sources in a specific state.",
        "query": "SELECT `State_Name`, `S_No`, `Sources_Found_Contaminated` FROM `ground_water_quality_testing` WHERE `State_Name` LIKE 'State_X%' AND `Sources_Found_Contaminated` > 0 ORDER BY `S_No`;"
    },
    {
        "input": "List the wells with the deepest groundwater levels in a specific state.",
        "query": "SELECT `Well_ID`, `State_Name`, `Well_Depth(meters)` FROM `ground_water_level_2015_to_2022` WHERE `State_Name` LIKE 'State_X%' ORDER BY `Well_Depth(meters)` DESC;"
    },
    {
        "input": "Compare water quality parameters for all monitoring locations in a specific state.",
        "query": "SELECT `Name of Monitoring Location`, `pH_Max`, `pH_Min`, `Conductivity_Max(μmhos/cm)`, `Conductivity_Min(μmhos/cm)`, `BOD_Max(mg/L)`, `BOD_Min(mg/L)`, `Nitrate_N_Max(mg/L)`, `Nitrate_N_Min(mg/L)`, `Fluoride_Max(mg/L)`, `Fluoride_Min(mg/L)`, `Arsenic_Max(mg/L)`, `Arsenic_Min(mg/L)` FROM `ground_water_quality_data` WHERE `State_Name` LIKE 'State_X%' ORDER BY `Name of Monitoring Location`;"
    },
    {
        "input": "Identify villages with the highest levels of a specific contaminant in a state.",
        "query": "SELECT `Village`, `State_Name`, `Fluoride`, `Total_Arsenic` FROM `village_water_contamination` WHERE `State_Name` LIKE 'State_X%' AND (`Fluoride` > 1.5 OR `Total_Arsenic` > 0.01) ORDER BY `Village`;"
    },
    {
        "input": "Provide details of remedial measures taken in contaminated areas of a specific state.",
        "query": "SELECT `State_Name`, `S_No`, `Remedial_Measures_Taken` FROM `ground_water_quality_testing` WHERE `State_Name` LIKE 'State_X%' AND `Remedial_Measures_Taken` > 0 ORDER BY `S_No`;"
    },
    {
        "input": "Retrieve the water quality testing status for a specific state.",
        "query": "SELECT `State_Name`, `Total_Sources`, `Sources_Tested`, `Sources_Yet_To_Be_Tested`, `Sources_Found_Safe`, `Sources_Found_Contaminated` FROM `ground_water_quality_testing` WHERE `State_Name` LIKE 'State_X%';"
    },
    {
        "input": "Find monitoring locations with the highest BOD levels in a specific state.",
        "query": "SELECT `Name of Monitoring Location`, `BOD_Max(mg/L)` FROM `ground_water_quality_data` WHERE `State_Name` LIKE 'State_X%' ORDER BY `BOD_Max(mg/L)` DESC;"
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



