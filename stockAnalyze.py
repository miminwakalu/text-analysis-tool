from datetime import date, datetime
from bs4 import BeautifulSoup
import requests
import yfinance as yf
import analyze
import json


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

    return {key: data.get(key, '') for key in keysToExtract}


def getPriceHistory(company):
    historyDf = company.history(period='12mo')

    return {
        'prices': historyDf['Open'].tolist(),
        'dates': historyDf.index.strftime('%Y-%m-%d').tolist()
    }


def getEarningsDate(company):
    earningsDatesDf = company.earnings_dates
    allDates = earningsDatesDf.index.strftime('%Y-%m-%d').tolist()

    dateObjects = [
        datetime.strptime(date_str, '%Y-%m-%d').date()
        for date_str in allDates
    ]

    currentDate = date.today()

    return [
        d.strftime('%Y-%m-%d')
        for d in dateObjects
        if d > currentDate
    ]


def getCompanyNews(company):
    allNewsArticles = []

    for newDict in company.news:
        link = newDict.get('link', '')
        if link:
            allNewsArticles.append({
                'title': newDict.get('title', ''),
                'link': link
            })

    return allNewsArticles


def extractNewsArticleTextFromHtml(soup):
    alltext = ''
    result = soup.find_all('div', {'class': 'caas-body'})

    for res in result:
        alltext += res.get_text(separator=' ', strip=True) + ' '

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

        try:
            page = requests.get(url, headers=headers, timeout=10)
            page.raise_for_status()
        except requests.RequestException:
            continue

        soup = BeautifulSoup(page.text, 'html.parser')

        if soup.find(string='Continue reading'):
            continue

        articleText = extractNewsArticleTextFromHtml(soup)
        allArticleTexts += articleText + ' '

    return allArticleTexts


def getCompanyStockInfo(tickerSymbol):
# Get data from yfinance API
    company = yf.Ticker(tickerSymbol)
# Get basic info on company
    basicInfo = extractBasicStockInfo(company.info)

# Check if company exist, if not, trigger error
    if not basicInfo['longName']:
        raise NameError('Could not find stock info, ticker may be delisted or does not exist.')

    priceHistory = getPriceHistory(company)
    futureEarningsDates = getEarningsDate(company)
    newsArticles = getCompanyNews(company)

    newsArticlesAllText = extractCompanyNewsArticles(newsArticles)
    newsTextAnalysis = analyze.analyzeText(
        newsArticlesAllText,
        tickerSymbol
    )

    return {
        'basicInfo': basicInfo,
        'priceHistory': priceHistory,
        'futureEarningsDates': futureEarningsDates,
        'newsArticles': newsArticles,
        'newsTextAnalysis': newsTextAnalysis
    }


# Example usage:
companyStockAnalysis = getCompanyStockInfo('MSFT')
print(json.dumps(companyStockAnalysis, indent=4))
