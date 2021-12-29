"""
This file is used for all JSON related functionality for entire project.
"""
import json
import logging as LOGGER

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
    LOGGER.info("Converted string values to dictionary.")
    info = dict([report.split(': ') for report in stringValue])
    return info

def convertcompanyToJSON(company):
    """
    This function will converts company information strings to JSON object.
    @param company
        List of strings having companies metadata
    @return companyMetaData
        JSON object of company's metadata
    """
    companyMetaData =  {
        "Name":company[0],
        "Market Cap":float(company[1]),
        "Current Price":float(company[2]),
        "Current High":float(company[3]),
        "Current Low":float(company[4]),
        "ROE":float(company[5]),
        "Divident Yield":float(company[6]),
        "Sector": company[7],
        "Stock Name": company[8],
        "Quarterly Results": convertToDictionary(company[9]),
        "Balance Sheet": convertToDictionary(company[10]),
        "Cash Flows": company[11]
        }
    LOGGER.info("Converted {} to schema format.".format(company[0]))
    return json.dumps(companyMetaData)

def convertcompanyToDictionaryList(companyList):
    """
    This function will converts list of JSON objects to list of dictionary items.
    @param companiesList
        List of JSON objects holding companies information
    @return companies
        List of dictionary values holding companies information
    """
    LOGGER.info("Converting JSON company list to python dictionary.")
    return json.load(companyList)