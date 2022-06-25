"""
This is the core file executing project files.
"""
import JSON_Dealer
import Company_Filtration
import Portfolio_Provider
import INFO
import CONSTANT
import time
from time import perf_counter
import multiprocessing
import pywhatkit
import logging.config
logging.config.dictConfig({
    'version': 1,
    'disable_existing_loggers': True,
})
logging.config.fileConfig(fname='ezMoneyLOGGER.conf')
LOGGER = logging.getLogger('root')

segments = INFO.marketSegments
if __name__ == '__main__':
    # Start time in seconds
    startTime = perf_counter()
    LOGGER.info("Started main process at {} with process limit {}".format(startTime, CONSTANT.processLimit))
    # Total companies to do analysis on
    companies = []
    # Set to handle duplications
    setOfCompanies = set()
    # Process pool 
    pool = multiprocessing.Pool(processes = CONSTANT.processLimit) # LIMIT FOR TK
    # Get company names for given segments
    results = pool.map(Portfolio_Provider.getCompanies, segments)
    for result  in results:
        companies+=result
    # Handle repetition of company names
    setOfCompanies.update(val for val in companies if val[0] not in [i[0] for i in setOfCompanies])
    # Flush old values
    totalNames = len(setOfCompanies)
    companies.clear()
    # Parse information for processing
    results = pool.map(Portfolio_Provider.parsingMethod, setOfCompanies)
    for result in results:
        companies.append(result)
    # Clear out invalid formats
    companies = list(filter(None, companies))
    totalCompaniesToProcess = len(companies)
    JSON_Dealer.jsonFileStore(companyList=companies, name="/logs/"+time.strftime("%Y-%m-%d-%H_%M_%S")+"coreProcess_companies.json", enList = False)
    # Total probable profitable companies
    profitableCompanies = []
    profitableCompanies = Company_Filtration.profitableCompanies(companies)
    totalProfitCompanies = len(profitableCompanies)
    for x in profitableCompanies:
        print(x['Name'], end=', ')
    JSON_Dealer.jsonFileStore(companyList=profitableCompanies, name="/logs/"+time.strftime("%Y-%m-%d-%H_%M_%S")+"coreProcess_profitableCompanies.json", enList = False)
    # End time in seconds
    endTime = perf_counter()
    LOGGER.info("Ended main process at {}".format(endTime))
    LOGGER.info("Total time taken for core process to run : {} minutes".format((endTime-startTime)/60))
    LOGGER.info("{names} names, {pro} processed companies, {selected} selected companies".format(names=totalNames, pro=totalCompaniesToProcess, selected=totalProfitCompanies))
    messageForWhatsapp = "Validate and invest in these stocks :\n"
    for kompany in profitableCompanies:
        messageForWhatsapp += (kompany['Name'])
        messageForWhatsapp += ", "
    messageForWhatsapp += "done!\nThis was done by {}".format(CONSTANT.versionName)
    # pywhatkit.sendwhatmsg_instantly("+919644049059", messageForWhatsapp, 30, True, 30)
    statusReport = "{names} names, {pro} processed companies, {selected} selected companies".format(names=totalNames, pro=totalCompaniesToProcess, selected=totalProfitCompanies)
    # pywhatkit.sendwhatmsg_instantly("+919644049059", statusReport, 30, True, 30)
    LOGGER.info("Iteration completed by version {} with process limit {} under .".format(CONSTANT.versionName, CONSTANT.processLimit))
    #L1 Filtration
    # filteredCompanies = Company_Filtration.profitableCompanies(JSON_Dealer.convertToJSONList(Portfolio_Provider.metadataCompanies()))
    #L2 Current Stock options
    # selectedStocks = Stock_Provider.stocksList(filteredCompanies)
    #L2 Filtration
    #Seasonality should be considered
    #Fucking wars should be considered
    #Timer should be put
    # !!! Type mismatch may occur