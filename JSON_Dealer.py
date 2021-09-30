"""
This file is used for all JSON related functionality for entire project.
"""
import json
# exampleCompanyStock =  {
#     "Name":"HLE Glascoat Ltd",      #NAME
#     "Market Cap":8589,              #Current Market Cap in crores
#     "Current Price":6381,           #Current price in INR
#     "Current High":6750,            #Current High in INR
#     "Current Low":1287,             #Current Low in INR
#     "ROE":41.4,                     #Current Return on Equity (profitability)
#     "Dividend Yield": "0.06",
#     "Sector": "Capital Goods-Non Electrical Equipment",
#     "Stock Name": "HLEGLAS",
#     "Quarterly Results":            #Should be of last 12 quarters
#     {
#         "OPM": [10, 9, 15, 16, 15, 18, 17, 17, 17, 22, 18, 19]
#         "Net Profit": [1, 3, 12, 7, 9, 11, 11, 6, 11, 17, 18, 14],
#         "EPS": [2.22, 2.22, 19.14, 11.51, 14.02, 8.38, 8.33, 4.80, 8.77, 12.94,	13.67, 10.55]
#     },
#     "Balance Sheet":                #Yearly balance reports in INR Crores
#     {
#         "Reserves": [10, 11, 13, 15, 18, 19, 21, 41, 45, 24, 52, 140],
#         "Fixed Assets": [19, 19,22, 22, 22, 20, 23, 26, 25, 80, 88, 114]
#     },
#     "Cash Flows": [-0, -0, 0, -0, -0, 0, -0, 1, 0, 5, -5, 9]   #Yearly Cash Flow in INR Crores
# }

def convertToDictionary(stringValue):
    """
    This function will return dictionary of strings.
    @param stringValue
        List of string values which needs conversion (Quarterly Results, Balance Sheets).
    @return dictionary
        Dictionary of the same.
    Example:
    I/P:[ (type is string)
        'OPM: [3, 6, 19, 14, 16, 18, 17, 12, 18, 25, 22, 22]', 
        'Net Profit: [1, 3, 12, 7, 9, 11, 11, 6, 11, 17, 18, 14]',
        'EPS: [2.22, 2.22, 19.14, 11.51, 14.02, 8.38, 8.33, 4.80, 8.77, 12.94,	13.67, 10.55]'
        ]
    O/P:{ (type is dictionary)
        "OPM": [3, 6, 19, 14, 16, 18, 17, 12, 18, 25, 22, 22],
        "Net Profit": [1, 3, 12, 7, 9, 11, 11, 6, 11, 17, 18, 14],
        "EPS": [2.22, 2.22, 19.14, 11.51, 14.02, 8.38, 8.33, 4.80, 8.77, 12.94,	13.67, 10.55]
        }
    """
    info = dict([report.split(': ') for report in stringValue])
    return info

def convertToJSONList(companiesList):
    """
    This function will converts list of company metadata strings to list of JSON objects.
    @param companiesList
        List of strings having companies metadata
    @return companies
        List of JSON objects holding companies information
    """
    companies = list()
    for company in companiesList:
        companyStock =  {
            "Name":company[0],
            "Market Cap":int(company[1]),
            "Current Price":int(company[2]),
            "Current High":int(company[3]),
            "Current Low":int(company[4]),
            "ROE":int(company[5]),
            "Current Price":int(company[6]),
            "Divident Yield":float(company[7]),
            "Sector": company[8],
            "Stock Name": company[9],
            "Quarterly Results": convertToDictionary(company[10]),
            "Balance Sheet": convertToDictionary(company[11]),
            "Cash Flows": json.loads(company[12])
            }
        companies.append(json.dumps(companyStock))

def convertToDictionaryList(companyList):
    """
    This function will converts list of JSON objects to list of dictionary items.
    @param companiesList
        List of JSON objects holding companies information
    @return companies
        List of dictionary values holding companies information
    """
    return json.load(companyList)