from datetime import date
from typing import Any
from datetime import datetime
import yfinance as yf
def extractBasicStockInfo(data):
    keysToExtract = [ 'longName', 'website', 'industry', 'marketCap', 'previousClose', 'totalRevenue', 'bookValue' ]
    basicInfo = {}
    for key in keysToExtract:
        if key in data:
            basicInfo[key] = data[key]
        else:
            basicInfo[key] = ''
    return basicInfo

def getPriceHistory(company):
    historyDf = company.history(period="12mo")
    prices = historyDf['Open'].tolist()
    dates = historyDf.index.strftime('%Y-%m-%d').tolist()
    print(dates)
    return {
        'prices': prices,
        'dates': dates
    }

def getEarningsDate(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime('%Y-%m-%d').tolist()
    dateObjects = [date.strptime(date_str, '%Y-%m-%d').date() for date_str in allDates]
    currentDate = date.today()
    futureDates = [date.strftime('%Y-%m-%d') for date in dateObjects if date > currentDate]
    return futureDates

def getCompanyNews(company):
    news = company.news
    allNewsArticles = []
    for newDict in news:
        newsDictToAddd = {
            'title': newDict['title'],
            'link': newDict['link']
        }
        allNewsArticles.append(newsDictToAddd)
    return allNewsArticles

def getCompanyStockInfo(tickerSymbol):
    # Get data from Yahool Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicStockInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)
   # print(priceHistory)

getCompanyStockInfo('MSFT')