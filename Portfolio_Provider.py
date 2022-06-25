"""
This file is used for web scraping companies and their required metadata.
Populate all required information from Screener.in website.
Current Limit is as per availability on first page of BSE.
"""
import JSON_Dealer
import CONSTANT
import time
import re
import itertools
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# Options TO HIDE
from selenium.webdriver.chrome.options import Options
# To suppress LOGS from imported modules
import logging
import logging.config
for _ in logging.root.manager.loggerDict:
    logging.getLogger(_).setLevel(level=logging.CRITICAL)
    logging.getLogger(_).disabled = True
# To suppress warnings from imported modules
import warnings
warnings.filterwarnings('ignore')
warnings.warn('DelftStack')
warnings.warn('Do not show this message')



logging.config.fileConfig(fname='ezMoneyLOGGER.conf')
LOGGER = logging.getLogger('PortfolioProvider')



def openWeb(url):
    """
    This function returns chrome driver opened with given url.
    @param : MANDATORY url
        URL to operate on
    @return driver
        Chrome driver
    """
    # Option to explicitly hide chrome in background.
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # Fix for chromium debugger printing annoying debugs
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=5') # Added with log level critical
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    chrome_options.binary_location = CONSTANT.CHROME_PATH
    driver = webdriver.Chrome(executable_path=CONSTANT.DRIVER_PATH, chrome_options=chrome_options)
    LOGGER.info("Chrome instance initialized for webdriver.")
    # URL on driver
    driver.get(url)
    # LOGGER.info("Loaded URL {}.".format(url))
    return driver

def getCompanies(marketSegment):
    """
    This function returns list of companies for given market segment.
    @param : MANDATORY marketSegment
        BSE Market Segment.
    @return companyNames
        List of names.
    """
    companyNames = []
    try :
        # Open webdriver of BSE
        driver = openWeb(CONSTANT.BSE_URL)
        # Find element which is dropdown menu for segment
        equityOption = driver.find_element_by_id('dllFilter2')
        selectEquity = Select(equityOption)
        selectEquity.select_by_value(marketSegment)
        LOGGER.info("Filtration done for {} segment.".format(marketSegment))
        # Induce lag because of hardware limitations :(
        time.sleep(10)
        # Table element containing list of all companies 
        listTable = driver.find_element_by_id('idTbody')
        # Row element containing information for one company
        listRows = listTable.find_elements_by_tag_name('tr')
        # List of companies under given segment
        for row in listRows:
            # Tag element containing name
            companyAttributes = row.find_element_by_tag_name('td')
            companyName = companyAttributes.find_element_by_tag_name('a')
            companyNames.append((companyName.text, marketSegment))
        LOGGER.info("Company names extracted for {}.".format(marketSegment))
        return companyNames
    except Exception as exc:
        print("Error in getCompanies for {} with error {}".format(marketSegment, str(exc)))
        return companyNames

def getValues(qResultElement, rowString):
    """
    This function returns string of given row.
    @param qResultElement
        Web Element containing table of attribute value.
    @param : MANDATORY rowString
        Web Element row name containing information.
    @return stringValue
        String format of list holding values of given row.
    """
    # Element table containing given attribute
    parentElement= qResultElement.find_element_by_xpath('//tr[.//*[contains(text(),"'+ rowString +'")]]')
    # List of obtained values
    valueList = parentElement.find_elements_by_tag_name('td')
    # Formatting
    stringValue = rowString + " : ["
    for value in valueList[1:-1]:
        tempVal = value.text
        tempVal = tempVal.replace(',', '')
        tempVal = tempVal.replace('%', '')
        stringValue += tempVal + ', '
    tempVal = valueList.pop().text
    tempVal = tempVal.replace(',', '')
    tempVal = tempVal.replace('%', '')
    stringValue += tempVal + ']'
    # LOGGER.info("Values extraction done.")
    return stringValue

def companyParser(company, sector):
    """
    This function returns formatted object of given company.
    @param : MANDATORY company
        Company name.
    @param : MANDATORY sector
        Sector of company.
    @return companyInfo
        JSON object of company.
    """
    try :
        # List of required information
        companyInfo = [company]
        LOGGER.info("Information extraction started for {}".format(company))
        # This is a workaround for hidden element on search section ->
        driver = openWeb(CONSTANT.SCREENER_URL+company+'/consolidated/')
        # Induce lag because of hardware limitations :(
        time.sleep(7)
        # Card element containing company's attributes  -> Fails when value is not present

        
        companyCard = driver.find_element_by_id('top-ratios')
        # Extracting values
        companyAttributes = companyCard.find_elements_by_xpath('.//span[contains(@class, "number")]')
        # Formatting
        for attribute in itertools.islice(companyAttributes, 4):
            companyInfo.append(attribute.text.replace(',', ''))
        companyInfo.append(companyAttributes[-2].text.replace(',', ''))
        companyInfo.append(companyAttributes[-4].text.replace(',', ''))
        companyInfo.append(sector)
        companyLinks = driver.find_element_by_class_name('company-links')
        companyInfo.append(re.sub(r'^.*?:', '', companyLinks.find_elements_by_tag_name('a')[2].text))

        stringOPMRatio = getValues(driver.find_element_by_id('quarters'), "OPM")    
        stringNetProfit = getValues(driver.find_element_by_id('quarters'), "Net Profit")
        stringEPS = getValues(driver.find_element_by_id('quarters'), "EPS")

        quarterlyResults = [stringOPMRatio, stringNetProfit, stringEPS]
        companyInfo.append(quarterlyResults)

        stringReserve = getValues(driver.find_element_by_id('balance-sheet'), "Reserves")
        stringFixedAssets = getValues(driver.find_element_by_id('balance-sheet'), "Fixed Assets")
        balanceSheet = [stringReserve, stringFixedAssets]
        companyInfo.append(balanceSheet)

        stringNetCashFlow = getValues(driver.find_element_by_id('cash-flow'), "Net Cash Flow")
        stringNetCashFlow = stringNetCashFlow.replace('Net Cash Flow : [', '')
        stringNetCashFlow = stringNetCashFlow.replace(']', '')
        stringNetCashFlow = stringNetCashFlow.replace(',', '')
        netCashFlow = list(stringNetCashFlow.split(" "))
        companyInfo.append(netCashFlow)
        LOGGER.info("Information extraction success for {}".format(company))
        return JSON_Dealer.convertcompanyToJSON(companyInfo)
    except Exception as exc:
        LOGGER.error("Error in companyParser for {company} with Error :{err}".format(company=company, err=str(str(exc))))
        CONSTANT.globalFailed.append(company)
        LOGGER.debug("Current value of failed list is {}".format(CONSTANT.globalFailed))
        return None

def parsingMethod(company):
    """
    This function returns formatted object of given company.
    @param : MANDATORY company
        Company tuple with name and sector values.
    @return companyInfo
        JSON object of company.
    """
    try:
        companyInfo = companyParser(company[0], company[1])
        return companyInfo
    except Exception as exc:
        LOGGER.error("Error inside Parsing method\n with message {}".format(str(str(exc))))
        CONSTANT.globalFailed.append(company[0])
        LOGGER.debug("Current value of failed list is {}".format(CONSTANT.globalFailed))
        return None