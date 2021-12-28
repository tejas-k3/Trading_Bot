"""
This file is used for web scraping companies and their required metadata.
Populate all required information from Screener.in website.
Current Limit is as per availability on first page of BSE.
"""
import time
import re
import itertools
from selenium import webdriver
from selenium.webdriver.support.ui import Select
# Options TO HIDE
from selenium.webdriver.chrome.options import Options

import JSON_Dealer
# Path to chrome binary
CHROME_PATH = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
# Path to chrome driver
DRIVER_PATH = 'C://Users//Tejas//Downloads//selenium//chromedriver.exe'
# URL to BSE Equity Market
BSE_URL = "https://www.bseindia.com/eqstreamer/StreamerMarketwatch.html"
# URL to Screener
SCREENER_URL = "https://www.screener.in/company/"

def openWeb(url):
    """
    This function returns chrome driver opened with given url.
    @param url
        URL to operate on
    @return driver
        Chrome driver
    """
    # Option to explicitly hide chrome in background.
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--window-size=%s" % "1920,1080")
    chrome_options.binary_location = CHROME_PATH
    # Chrome instance for webdriver
    driver = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=chrome_options)
    # URL on driver
    driver.get(url)

    return driver

def getCompanies(marketSegment):
    """
    This function returns list of companies for given market segment.
    @param marketSegment
        BSE Market Segment.
    @return companyNames
        List of names.
    """
    # Open webdriver of BSE
    driver = openWeb(BSE_URL)
    # Find element which is dropdown menu for segment
    equityOption = driver.find_element_by_id('dllFilter2')
    selectEquity = Select(equityOption)
    selectEquity.select_by_value(marketSegment)
    # Induce lag because of hardware limitations :(
    time.sleep(10)
    # Table element containing list of all companies 
    listTable = driver.find_element_by_id('idTbody')
    # Row element containing information for one company
    listRows = listTable.find_elements_by_tag_name('tr')
    # List of companies under given segment
    companyNames = []
    for row in listRows:
        # Tag element containing name
        companyAttributes = row.find_element_by_tag_name('td')
        companyName = companyAttributes.find_element_by_tag_name('a')
        companyNames.append(companyName.text)

    return companyNames

def getValues(qResultElement, rowString):
    """
    This function returns string of given row.
    @param qResultElement
        Web Element containing table of attribute value.
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

    return stringValue

def companyParser(company, sector):
    """
    This function returns formatted object of given company.
    @param company
        Company name.
    @param sector
        Sector of company.
    @return companyInfo
        JSON object of company.
    """
    # List of required information
    companyInfo = [company]
    # This is a workaround for hidden element on search section ->
    driver = openWeb(SCREENER_URL+company+'/consolidated/')
    # Induce lag because of hardware limitations :(
    time.sleep(10)
    # Card element containing company's attributes
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
    return JSON_Dealer.convertcompanyToJSON(companyInfo)