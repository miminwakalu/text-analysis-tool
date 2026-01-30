from datetime import date
from typing import Any
from datetime import datetime
from bs4 import BeautifulSoup
import requests
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
    historyDf = company.history(period='12mo')
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

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                  'AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/120.0.0.0 Safari/537.36'
}
def extractCompanyNewsArticles(newsArticles):
    for newsArticle in newsArticles:
        url = newsArticle['link']
        page = requests.get(url, headers=headers)
        print(page.text)
        soup = BeautifulSoup(page.text, 'html.parser')
        print(soup.prettify())
        print(url)
        if soup.findAll(string = 'Continue reading'):
            print('Tag found - should skip')
        else:
            print('Tag not found - should not skip')

def getCompanyStockInfo(tickerSymbol):
    # Get data from Yahool Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicStockInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)
   

getCompanyStockInfo('MSFT')