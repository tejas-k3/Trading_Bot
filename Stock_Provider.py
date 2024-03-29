"""
This file is used for web scraping stock and associated required data.
Populate all required information from screener.in and moneycontrol.com websites.
Current Limit is 10 ie gather relevant information of 10 stocks.
"""
import DataParser
import logging
import logging.config
logging.config.fileConfig(fname='ezMoneyLOGGER.conf')
LOGGER = logging.getLogger('StockProvider')


def stockInformation(company):
    """
    This function will return stock information of company.
    @param company
        Name of company.
    @return stock
        JSON Object of stock.
    """
    # Web scraping for stock
    stock = []
    # Populate above variable
    return DataParser.convertToDictionary(stock)
    

def stocksList(companyList):
    """
    This function will return stock information of company.
    @param company
        List of companies.
    @return stock
        List of stock values as dictionary.
    """
    for company in companyList:
        stocks = list()
        stocks.append(stockInformation(company))
    return stocks
