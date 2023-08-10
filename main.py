from twilio.rest import Client
import requests
import os

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ACCOUNT_SID = os.environ["TWILIO_SID"]
AUTH_TOKEN = os.environ["TWILIO_AUTH"]
SENDER_PHONE_NUMBER = os.environ["S_NO"]
RECIEVER_PHONE_NUMBER = os.environ["R_NO"]

STOCK_API_KEY = os.environ["S_KEY"]
NEWS_API_KEY = os.environ["N_KEY"]

stock_params = {
    "function": "TIME_SERIES_DAILY_ADJUSTED",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY
}

response = requests.get(STOCK_ENDPOINT, stock_params)

data = response.json()["Time Series (Daily)"]

data_list = [value for (key, value) in data.items()]
yesterday_data = data_list[0]
yesterday_market_close = yesterday_data["4. close"]

day_before_yesterday = data_list[1]
day_before_yesterday_close = day_before_yesterday["4. close"]

difference = abs(float(yesterday_market_close)-float(day_before_yesterday_close))

if difference > 0:
    up_down = "🔺"
else:
    up_down = "🔻"

percentage_difference = round((difference/float(yesterday_market_close))*100)

if percentage_difference > 2:
    news_params = {
        "apiKey": NEWS_API_KEY,
        "qInTitle": COMPANY_NAME
    }
    news_response = requests.get(NEWS_ENDPOINT, news_params)
    articles = news_response.json()["articles"]

    three_articles = articles[:3]

    formatted_articles = [f"{STOCK_NAME}: {up_down}{percentage_difference}%\nHeadline: {article['title']}. \nBreif: {article['description']}" for article in three_articles]

    client = Client(ACCOUNT_SID, AUTH_TOKEN)

    for article in formatted_articles:
        message = client.messages.create(
            body= article,
            from_= SENDER_PHONE_NUMBER,
            to= RECIEVER_PHONE_NUMBER
        )
