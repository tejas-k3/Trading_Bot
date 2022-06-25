from ast import Constant
import Portfolio_Provider
import Company_Filtration
from time import perf_counter
import pywhatkit
import CONSTANT
import INFO
import logging
import logging.config
logging.config.fileConfig(fname='ezMoneyLOGGER.conf')
LOGGER = logging.getLogger('root')

# segmentList = INFO.marketSegments

segmentList = []
segmentList.append('S&P BSE Consumer Discretionary Goods & Services')
segmentList.append('S&P BSE Telecom')
# segmentList.append('S&P BSE India Manufacturing Index')
# segmentList.append('S&P BSE Fast Moving Consumer Goods')
# segmentList.append('S&P BSE BANKEX')
# segmentList.append('S&P BSE 250 LargeMidCap Index')

companies = []

def parsingMethod(companiesList):

    try:
        val = Portfolio_Provider.companyParser(companiesList[0], companiesList[1])
        # Appending companies wasnt working here because of localized code.
        LOGGER.info("Parsed companies.")
        return val
    except Exception:
        LOGGER.error("Error inside Parsing method")
    
import multiprocessing
######################## 1112.3271719 optimised and current time 364.4034104
if __name__ == '__main__':
    t1_start = perf_counter()
    tempval = []
    setOfCompanies = set()
    pool = multiprocessing.Pool(processes = CONSTANT.processLimit) # 53 for 3pid, 4 segments 3 was for i5 8GEN
    results = pool.map(Portfolio_Provider.getCompanies, segmentList)
    for result  in results:
        tempval+=result
    setOfCompanies.update(val for val in tempval if val[0] not in [i[0] for i in setOfCompanies])
    LOGGER.info("Scrapped company names.")
    # print(len(setOfCompanies), "After duplication removal", setOfCompanies)
    results = pool.map(parsingMethod, setOfCompanies)
    for result in results:
        companies.append(result)
    companies = list(filter(None, companies))
    LOGGER.info("Scrapped companies information and saved it in a list.")
    profitable = []
    profitable = Company_Filtration.profitableCompanies(companies)
    # JSON_Dealer.jsonFileStore(companyList=profitable, name="/profitableCompanies.json")
    t1_end = perf_counter()
    print("Total time taken in mins : ", (t1_end-t1_start)/60)
    print("Failed for following :")
    
    # print(CONSTANT.globalFailed)
    # messageForWhatsapp = "Potential buy stock names\n"
    # for kompany in profitable:
    #     messageForWhatsapp += (kompany['Name'] + " at price  " + str(kompany['Current Price']))
    #     messageForWhatsapp  += ('\n')
    # print(messageForWhatsapp)
    # pywhatkit.sendwhatmsg_instantly("+919644049059", messageForWhatsapp, 10, True, 20)



#################

