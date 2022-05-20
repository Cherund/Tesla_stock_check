import requests
from twilio.rest import Client

ACCOUNT_SID = YOUR-ACCOUNT-ID
AUTH_TOKEN = YOUR-TOKEN

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = YOUR-STOCK-API-KEY
NEWS_API_KEY = YOUR-NEW-API-KEY

stock_parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': STOCK_API_KEY
}

news_parameters = {
    'apiKey': NEWS_API_KEY,
    'q': 'Tesla'
}

stock_response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
stock = stock_data['Time Series (Daily)']
two_days_stock = [value['4. close'] for (key, value) in stock.items()][:2]
yesterday_stock = float(two_days_stock[0])
day_before_yesterday_stock = float(two_days_stock[1])

difference = abs(yesterday_stock-day_before_yesterday_stock)
one_pers = yesterday_stock*0.01

change_in_pers = round(difference / one_pers, 2)

if yesterday_stock > day_before_yesterday_stock:
    change = f'TSLA: 🔺{change_in_pers}%'
else:
    change = f'TSLA: 🔻{change_in_pers}%'

print(change)

if difference >= one_pers:
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    three_articles = news_response.json()['articles'][:3]

    formatted_articles = [
        f"{change}\nHeadline: {article['title']}. \nBrief: {article['description']}"
        for article in three_articles]


    for article in formatted_articles:
    
        client = Client(ACCOUNT_SID, AUTH_TOKEN)
        message = client.messages \
            .create(
            body=f'{article}',
            from_='+19896621866',
            to='+79953892311'
        )
        print(message.status)
