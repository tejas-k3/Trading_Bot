import Portfolio_Provider
import Company_Filtration
import logging as LOGGER
from time import perf_counter
import pywhatkit
segmentList = []

segmentList.append('S&P BSE Consumer Discretionary Goods & Services')
segmentList.append('S&P BSE Telecom')
segmentList.append('S&P BSE India Manufacturing Index')
segmentList.append('S&P BSE Fast Moving Consumer Goods')



companies = []
LOGGER.info("Received BSE segment to work with.")

def parsingMethod(companiesList):

    try:
        val = Portfolio_Provider.companyParser(companiesList[0], companiesList[1])
        # Appending companies wasnt working here
        return val
    except Exception:
        print("Error inside Parsing method")
    
import multiprocessing
######################## 1112.3271719 optimised and current time 364.4034104
if __name__ == '__main__':
    t1_start = perf_counter()
    tempval = []
    setOfCompanies = set()
    pool = multiprocessing.Pool(processes = 3) # 53 for 3pid, 4 segments
    results = pool.map(Portfolio_Provider.getCompanies, segmentList)
    for result  in results:
        tempval+=result
    setOfCompanies.update(val for val in tempval if val[0] not in [i[0] for i in setOfCompanies])
    # print(len(setOfCompanies), "After duplication removal", setOfCompanies)
    results = pool.map(parsingMethod, setOfCompanies)
    for result in results:
        companies.append(result)
    companies = list(filter(None, companies))
    profitable = []
    profitable = Company_Filtration.profitableCompanies(companies)
    # JSON_Dealer.jsonFileStore(companyList=profitable, name="/profitableCompanies.json")
    t1_end = perf_counter()
    print("Total time taken : ", t1_end-t1_start)
    messageForWhatsapp = "Potential buy stock names\n"
    for kompany in profitable:
        messageForWhatsapp += (kompany['Name'])
        messageForWhatsapp  += ('\n')
    pywhatkit.sendwhatmsg_instantly("+919644049059", messageForWhatsapp, 10, True, 20)



#################




LOGGER.info("Scrapped company names.")
# companies.append(Portfolio_Provider.companyParser('MARUTI', 'S&P BSE AUTO'))
LOGGER.info("Scrapped companies information and saved it in a list.")



# print("Total companies to process ", len(companies))
# print("Total worthy companies ", len(profitable))

# with open(os.getcwd() + "/profitableCompanies.json", "w+") as companiesFile:
#     companiesFile.write("[")
#     companiesFile.write(str(profitable))
#     companiesFile.write("]")
# for kompany in profitable:
#     print(type(kompany))
#     print(kompany)
LOGGER.info("Saved the companies information in companie.json file under working directory.")
