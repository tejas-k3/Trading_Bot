import JSON_Dealer
import Company_Filtration
import Portfolio_Provider
"""
This is the core file making entire process work.
"""
Company_Filtration(JSON_Dealer.convertToJSONList(Portfolio_Provider.metadataCompanies()))
