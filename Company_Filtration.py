"""
This file holds logic for filtration of companies based on metric evaluation.
* Introduce LONGTERM, INTRADAY, SHORTTERM variations with approx TIME
"""
import itertools as it
from CONSTANT import *
import logging
import logging.config
logging.config.fileConfig(fname='ezMoneyLOGGER.conf')
LOGGER = logging.getLogger('CompanyFilteration')

# Shortfall (Coverage)
# Need to create for list of companies having 0 OPM

def profitableCompanies(companies):
    """
    This function will filter companies.
    @param : MANDATORY companies
        List of JSON companies
    @return : MANDATORY potentialCompanies
        List of JSON potential companies
    """
    potentialCompanies = []
    for company in companies:
        if isProfitable(company):
            potentialCompanies.append(company)
    LOGGER.info("Processed profitable company.")
    # Adding iteration number would be great.
    return potentialCompanies

def isProfitable(company):
    """
    This function will validate companies.
    @param : MANDATORY company
        JSON company
    @return : True/False
    """
    if confidentROE(company['ROE'])*confidentOPM(company["Quarterly Results"]['OPM'])*confidentDividendYield(company['Divident Yield']):
        return True
    return False

def confidentROE(ROE):
    if ROE>=ROELowerLimit and ROE<=ROEUpperLimit:
        return ROE_HighlyConfidenceValue
    elif ROE>ROEUpperLimit:
        LOGGER.debug("Fairly Confident ROE")
        return ROE_FairlyConfidenceValue
    LOGGER.debug("Not Confident ROE")
    return 0

def confidentOPM(OPMList):
    growthValue = 0
    while 0.0 in OPMList:
        OPMList.remove(0.0)
    while -0.0 in OPMList:
        OPMList.remove(-0.0)
    try:
        growthRate=[((x-y)*100)/y for x, y in zip(OPMList[1:], OPMList)]
        for value in growthRate:
            growthValue+=value
        if growthValue < OPMLimit and OPMList[0] <= OPMLimit:
            # print(growthValue, "OPM Growth value")
            return OPM_HighlyConfidenceValue
        return -1
    except Exception as exc:
            LOGGER.error("OPM Analysis error for OPM {oplist} with {err}".format(oplist=OPMList, err=str(exc)))
            return -1
    # if growthValue > OPMLimit and OPMList[0] <= OPMLimit:

def confidentDividendYield(dividendYield):
    if dividendYield>=dividendYieldLowerLimit and dividendYield<=dividendYieldUpperLimit:
        return dividendYield_HighlyConfidenceValue
    elif dividendYield>dividendYieldUpperLimit:
        return dividendYield_FairlyConfidenceValue
    return 0

# Needs dev
def shareholdingPattern(holdingValues):
    # Stable holding of promoters 40, FII (Financial Institutional Investors) 30-35, DII (Domestic Institutional Investors) 15
    holdingValues['promoters']
    return True
    
def confidentROCE(ROCE):
    if ROCE>=ROCELowerLimit and ROCE<=ROCEUpperLimit:
        return ROCE_HighlyConfidenceValue
    elif ROCE>ROCEUpperLimit:
        LOGGER.debug("Fairly Confident ROCE")
        return ROCE_FairlyConfidenceValue
    LOGGER.debug("Not Confident ROCE")
    return 0

# Needs dev
def confidentPBV(PBV):
    # < 1 means undervalued.
    # Mostly applicable on companies with liquid assets
    return True

# Needs dev
def confidentDER(DBR):
    # Debt to Equity Ratio
    # _low_ ASSUME more scope of expansion. _high_ ASSUME company invested in high NPV projects (NET PRESENT VALUE)
    return True

# Needs dev
def confidentEVEB(EVEB):
    # USE WITH PE!!!
    # low means underrated BUT RATIO FOR FAST GROWING INDUSTRIES IS KINDA HIGH.
    return True

# Needs dev
def confidentPE(PE, industryPE, marketPE):
    # Compare with historic, < industry and < market.
    return True

# Needs dev
def confidentCurrentRatio(currentRatio):
    # Less than 1 is major concern
    # How well equipped is company in meeting its short term goals.
    return True

# Needs dev
def confidentATR(ATR):
    # Asset turn over Ratio, compare with peers, more better.
    return True

# Needs dev
def confidentMarketValue(marketValue):
    # MarketCap/Book Value (Ratio per year comparison)
    return True
