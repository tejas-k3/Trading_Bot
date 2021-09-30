"""
This is the core file executing project files.
"""
import JSON_Dealer
import Company_Filtration
import Portfolio_Provider
import Stock_Provider
#L1 Filtration
filteredCompanies = Company_Filtration.profitableCompanies(JSON_Dealer.convertToJSONList(Portfolio_Provider.metadataCompanies()))
#L2 Current Stock options
selectedStocks = Stock_Provider.stocksList(filteredCompanies)
#L2 Filtration
#Seasonality should be considered
#Timer should be put
# !!! Type mismatch may occur