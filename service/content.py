import requests
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())
URL = os.getenv("URL")
TOKEN = os.getenv("TOKEN")


def get_data():
    """Sheety API Manage"""
    headers = {
        "Authorization": f"Bearer {TOKEN}"
    }

    res = requests.get(url=URL, headers=headers)
    res.raise_for_status()
    return res.json()
