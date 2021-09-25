"""
This file holds logic for filtration of companies based on metric evaluation.
"""

def profitableCompany(companies):
    potentialCompanies = list()
    for company in companies:
        if isProfitable(company):
            potentialCompanies.append(company)
    return potentialCompanies

def isProfitable(company):
    if True:
        return True
    else:
        return False