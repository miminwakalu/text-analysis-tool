import yfinance as yf

def extractBasicStockInfo(data):
    keysToExtract = [ 'longName', 'website', 'industry', 'marketCap', 'previousClose', 'totalRevenue', 'bookValue' ]
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ""
    return basicInfo

def getCompanyStockInfo(tickerSymbol):
    company = yf.Ticker(tickerSymbol)
    basicInfo = extractBasicStockInfo(company.info)
    print(basicInfo)

getCompanyStockInfo("MSFT")