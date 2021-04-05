import requests
from bs4 import BeautifulSoup
import lxml
from random import choice
import re

with open('input/user_agents.txt', mode="r") as file:
    user_agents = file.read().split("\n")


headers = {
    'authority': 'www.amazon.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'dnt': '1',
    'upgrade-insecure-requests': '1',
    'user-agent': choice(user_agents),
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'sec-fetch-site': 'none',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
}


def price_filter(get_price: str):
    if "€" in get_price:
        get_price = get_price.replace(".", "").split("\xa0€")[0].replace("\xa0€", "").replace(",", ".")
        return get_price
    elif "$" in get_price:
        get_price = get_price.replace(",", "").replace("US$\xa0", "")
        return get_price


def amz_price_verifier(url_amz):
    response = requests.get(url=url_amz, headers=headers)
    response.raise_for_status()
    amazon_data = response.text
    soup = BeautifulSoup(amazon_data, "lxml")
    product_title = soup.select(selector="#productTitle")[0].getText()
    asin = re.findall(r"dp/B\w*", url_amz, re.IGNORECASE)[0]
    country = re.findall(r"amazon\.\w*/", url_amz, re.IGNORECASE)[0]
    amz_buy_url = country + asin

    if len(soup.select(selector="#price_inside_buybox")) != 0:
        get_price = soup.select(selector="#price_inside_buybox")[0].getText()
        return float(price_filter(get_price)), product_title, amz_buy_url
    elif len(soup.select(selector="#priceblock_ourprice")) != 0:
        get_price = soup.select(selector="#priceblock_ourprice")[0].getText()
        return float(price_filter(get_price)), product_title, amz_buy_url
    elif len(soup.select(selector="#newBuyBoxPrice")) != 0:
        get_price = soup.select(selector="#newBuyBoxPrice")[0].getText()
        return float(price_filter(get_price)), product_title, amz_buy_url
    elif len(soup.select(selector="#priceblock_dealprice")) != 0:
        get_price = soup.select(selector="#priceblock_dealprice")[0].getText()
        return float(price_filter(get_price)), product_title, amz_buy_url
    elif len(soup.select(selector="#priceblock_saleprice")) != 0:
        get_price = soup.select(selector="#priceblock_saleprice")[0].getText()
        return float(price_filter(get_price)), product_title, amz_buy_url
    else:
        return None, None, None
