from datetime import date, datetime
from typing import Any
from bs4 import BeautifulSoup
import requests
import yfinance as yf


def extractBasicStockInfo(data):
    keysToExtract = [
        'longName',
        'website',
        'industry',
        'marketCap',
        'previousClose',
        'totalRevenue',
        'bookValue'
    ]
    basicInfo = {}

    for key in keysToExtract:
        basicInfo[key] = data.get(key, '')

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

    # ✅ FIXED HERE: use datetime.strptime, not date.strptime
    dateObjects = [
        datetime.strptime(date_str, '%Y-%m-%d').date()
        for date_str in allDates
    ]

    currentDate = date.today()

    futureDates = [
        d.strftime('%Y-%m-%d')
        for d in dateObjects
        if d > currentDate
    ]

    return futureDates


def getCompanyNews(company):
    news = company.news
    allNewsArticles = []

    for newDict in news:
        newsDictToAdd = {
            'title': newDict.get('title', ''),
            'link': newDict.get('link', '')
        }

        # Skip items that don't have a link
        if newsDictToAdd['link']:
            allNewsArticles.append(newsDictToAdd)

    return allNewsArticles

def extractNewsArticleTextFromHtml(soup):
    result = soup.find_all('div', {'class':'caas-body'})
    for res in result:
        print(res.text)
        alltext += res.text
    return alltext

headers = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    )
}


def extractCompanyNewsArticles(newsArticles):
    allArticleTexts = ''
    for newsArticle in newsArticles:
        url = newsArticle['link']
        page = requests.get(url, headers=headers)

        soup = BeautifulSoup(page.text, 'html.parser')

        if not soup.find_all(string='Continue reading'):
            print('Tag found - should skip')
        else:
            print('Tag not found - should not skip')
            articleText = extractNewsArticleTextFromHtml(soup)
    return allArticleTexts

def getCompanyStockInfo(tickerSymbol):
    # Get data from Yahoo Finance API
    company = yf.Ticker(tickerSymbol)

    # Get basic info on company
    basicInfo = extractBasicStockInfo(company.info)
    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)
    newsArticlesAllText = extractCompanyNewsArticles(newsArticles)
    print(newsArticlesAllText)

    return {
        'basicInfo': basicInfo,
        'priceHistory': priceHistory,
        'futureEarningsDates': futureEarningsDates,
        'newsArticles': newsArticles
    }


getCompanyStockInfo('MSFT')
