"""
This file holds logic for filtration of companies based on metric evaluation.
"""
import itertools as it

# Configurable variables for tuning the logic to have better confidence
ROELowerLimit=15
ROEUpperLimit=20
ROE_HighlyConfidenceValue = 1.5
ROE_FairlyConfidenceValue = 1.0
OPMLimit = 0.05
OPM_HighlyConfidenceValue = 1.0
dividendYieldLowerLimit = 0.40
dividendYieldUpperLimit = 0.75
dividendYield_HighlyConfidenceValue = 1.5
dividendYield_FairlyConfidenceValue = 1.0

def profitableCompanies(companies):
    """
    This function will filter companies.
    @param companies
        List of JSON companies
    @return potentialCompanies
        List of JSON potential companies
    """
    potentialCompanies = list()
    for company in companies:
        if isProfitable(company):
            potentialCompanies.append(company)
    return potentialCompanies

def isProfitable(company):
    if confidentROE(company["ROE"])*confidentOPM(company["Quarterly Results"["OPM"]])*confidentDividendYield(company["Divident Yield"]):
        return True
    return False

def confidentROE(ROE):
    if ROE>=ROELowerLimit and ROE<=ROEUpperLimit:
        return ROE_HighlyConfidenceValue
    elif ROE>ROEUpperLimit:
        #"Fairly Confident"
        return ROE_FairlyConfidenceValue
    #"Not Confident"
    return 0

def confidentOPM(OPMList):
    growthValue = 0
    growthRate=[(x-y)*100/y for x, y in it.izip(OPMList[1:], OPMList)]
    for value in growthRate:
        growthValue+=value
    if growthValue>OPMLimit and OPMList[0]<=OPMLimit[-1]:
        return OPM_HighlyConfidenceValue
    return -1

def confidentDividendYield(dividendYield):
    if dividendYield>=dividendYieldLowerLimit and dividendYield<=dividendYieldUpperLimit:
        return dividendYield_HighlyConfidenceValue
    elif dividendYield>dividendYieldUpperLimit:
        return dividendYield_FairlyConfidenceValue
    return 0
