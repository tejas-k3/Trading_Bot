"""
This is the core file executing project files.
"""
import JSON_Dealer
import Company_Filtration
import Portfolio_Provider

#L1 Filtration
Company_Filtration.profitableCompany(JSON_Dealer.convertToJSONList(Portfolio_Provider.metadataCompanies()))
#L2 Current Option

#Seasonality should be considered
#Timer should be put