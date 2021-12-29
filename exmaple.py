import Portfolio_Provider
import os
import logging as LOGGER

segment = 'S&P BSE AUTO'
LOGGER.info("Received BSE segment to work with.")
companyNames = Portfolio_Provider.getCompanies(segment)
LOGGER.info("Scrapped company names.")
companies = ""
for company in companyNames[0:-1]:
    companies += Portfolio_Provider.companyParser(company, segment)
    companies += ", "
companies += Portfolio_Provider.companyParser(companyNames[-1], segment)
LOGGER.info("Scrapped companies information and saved it in a list.")
with open(os.getcwd() + "/companies.json", "w+") as companiesFile:
    companiesFile.write("[")
    companiesFile.write(companies)
    companiesFile.write("]")
LOGGER.info("Saved the companies information in companie.json file under working directory.")
