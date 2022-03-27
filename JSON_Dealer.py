"""
This file is used for all JSON related functionality for entire project.
"""
import json
import os
import CONSTANT

# logging.config.fileConfig(fname='ezMoney#LOGGER.conf')
#LOGGER = logging.get#LOGGER('JSONDealer')


def convertToDictionary(stringValue):
    """
    This function will return dictionary of strings.
    @param : MANDATORY stringValue
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
    #LOGGER.info("Converted string values to dictionary.")
    info = {}
    for record in stringValue:
        pairValue = list(record.split(' : '))
        pairValue[1] = pairValue[1].replace('[', '')
        pairValue[1] = pairValue[1].replace(']', '')
        pairValue[1] = list(map(float, list(pairValue[1].split(', '))))
        info[pairValue[0]] = pairValue[1]
    return info

def convertcompanyToJSON(company):
    """
    This function will converts company information strings to JSON object.
    @param : MANDATORY company
        List of strings having companies metadata
    @return companyMetaData
        JSON object of company's metadata
    """
    if company==None:
        print("JSON Dealer returns None")
        return None

    # Covering the case where value is not available.
    for val in range(0, 12):
        if company[val]=='':
            print("For {name}, index {i} was having val {x}!".format(name=company[0], i=val, x=company[val]))
            company[val]='0'

    try :
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
        #LOGGER.info("Converted {} to schema format.".format(company[0]))
        return companyMetaData
    except Exception as exc:
        CONSTANT.globalFailed.append(company[0])
        print("Error in company Meta schema conversion for {name} with error:\n{err}".format(name = company[0], err=str(exc)))
        print("Current failed companies ")
        return None

def jsonFileStore(companyList, path=None, name=None, enList=True):
    """
    This function will converts list of JSON objects to list of dictionary items.
    @param : MANDATORY companiesList
        List of JSON objects holding companies information
    @param : OPTIONAL path
        Path where file will be saved.
    @param : OPTIONAL name
        Name of file to be stored.
    """
    #LOGGER.info("Converting JSON company list to python dictionary.")
    if path is None:
        path = os.getcwd()
    if name is None:
        name = "/values.json"
    try :
        with open( path+name, "w+") as jsonFile:
            if(enList):
                jsonFile.write("[")
            jsonFile.write(json.dumps(companyList))
            if(enList):
                jsonFile.write("]")
    except Exception:
        os.remove(path+name)
        print("Error in file creation with {err}".format(str(Exception)))