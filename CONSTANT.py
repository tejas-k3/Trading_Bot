import os
# Project CONSTANTS
versionName = "Dev_V1.0.0.1"

#Hardware limitation :(
# processLimit = 3 # For i5 8th Gen
processLimit = 16 # i7 11Gen at min



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
ROCELowerLimit = 0
ROCEUpperLimit = 50
ROCE_HighlyConfidenceValue = 1.5
ROCE_FairlyConfidenceValue = 0.75

globalFailed=[]


"""Links and system variables"""
# Path to chrome binary
CHROME_PATH = r'C:/Program Files/Google/Chrome/Application/chrome.exe'
# Path to chrome driver
DRIVER_PATH = os.getcwd()+'//ExcecutableDependencies//chromedriver.exe'
# URL to BSE Equity Market
BSE_URL = "https://www.bseindia.com/eqstreamer/StreamerMarketwatch.html"
# URL to Screener
SCREENER_URL = "https://www.screener.in/company/"