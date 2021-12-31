import Portfolio_Provider
import Company_Filtration
import logging as LOGGER
from time import perf_counter

segmentList = []
segmentList.append('S&P BSE SENSEX')
segmentList.append('S&P BSE 100')
segmentList.append('S&P BSE 100 ESG Index')
segmentList.append('S&P BSE 100 LargeCap TMC Index')
segmentList.append('S&P BSE 150 MidCap Index')
segmentList.append('S&P BSE 200')
segmentList.append('S&P BSE 250 LargeMidCap Index')
segmentList.append('S&P BSE 250 SmallCap Index')
segmentList.append('S&P BSE 400 MidSmallCap Index')
segmentList.append('S&P BSE 500')
segmentList.append('S&P BSE AllCap')
segmentList.append('S&P BSE AUTO')
segmentList.append('S&P BSE BANKEX')
segmentList.append('S&P BSE Basic Materials')
segmentList.append('S&P BSE Bharat 22 Index')
segmentList.append('S&P BSE CAPITAL GOODS')
segmentList.append('S&P BSE CARBONEX')
segmentList.append('S&P BSE Consumer Discretionary Goods & Services')
segmentList.append('S&P BSE CONSUMER DURABLES')
segmentList.append('S&P BSE CPSE')
segmentList.append('S&P BSE Diversified Financials Revenue Growth Index')
segmentList.append('S&P BSE Dividend Stability Index')
segmentList.append('S&P BSE DOLLEX 100')
segmentList.append('S&P BSE DOLLEX 200')
segmentList.append('S&P BSE DOLLEX 30')
segmentList.append('S&P BSE Energy')
segmentList.append('S&P BSE Enhanced Value Index')
segmentList.append('S&P BSE Fast Moving Consumer Goods')
segmentList.append('S&P BSE Finance')
segmentList.append('S&P BSE GREENEX')
segmentList.append('S&P BSE Healthcare')
segmentList.append('S&P BSE India Infrastructure Index')
segmentList.append('S&P BSE India Manufacturing Index')
segmentList.append('S&P BSE Industrials')
segmentList.append('S&P BSE Information Technology')
segmentList.append('S&P BSE IPO')
segmentList.append('S&P BSE LargeCap')
segmentList.append('S&P BSE Low Volatility Index')
segmentList.append('S&P BSE METAL')
segmentList.append('S&P BSE MidCap')
segmentList.append('S&P BSE MidCap Select Index')
segmentList.append('S&P BSE Momentum Index')
segmentList.append('S&P BSE OIL & GAS')
segmentList.append('S&P BSE POWER')
segmentList.append('S&P BSE Private Banks Index')
segmentList.append('S&P BSE PSU')
segmentList.append('S&P BSE Quality Index')
segmentList.append('S&P BSE REALTY')
segmentList.append('S&P BSE SENSEX 50')
segmentList.append('S&P BSE SENSEX Next 50')
segmentList.append('S&P BSE SmallCap')
segmentList.append('S&P BSE SmallCap Select Index')
segmentList.append('S&P BSE SME IPO')
segmentList.append('S&P BSE TECK')
segmentList.append('S&P BSE Telecom')
segmentList.append('S&P BSE Utilities')

# segmentList.append('S&P BSE Consumer Discretionary Goods & Services')
# segmentList.append('S&P BSE Healthcare')
# segmentList.append('S&P BSE India Manufacturing Index')
# segmentList.append('S&P BSE SmallCap')



companies = []
LOGGER.info("Received BSE segment to work with.")

def parsingMethod(companiesList):

    try:
        val = Portfolio_Provider.companyParser(companiesList[0], companiesList[1])
        # Appending companies wasnt working here
        return val
    except Exception:
        print("Error inside Parsing method")
    
import JSON_Dealer
import multiprocessing
from itertools import zip_longest
######################## 1112.3271719
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
    print(profitable)
    JSON_Dealer.jsonFileStore(companyList=profitable, name="/profitableCompanies.json")
    t1_end = perf_counter()
    print("Total time taken : ", t1_end-t1_start)



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
