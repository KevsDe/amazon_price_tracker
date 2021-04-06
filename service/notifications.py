import smtplib
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())
MY_EMAIL = os.getenv("MY_EMAIL")
PASSWORD = os.getenv("PASSWORD")
RECEIPT_EMAIL = os.getenv("RECEIPT_EMAIL")


def send_email(message):
    """This function will send an email with a custom message"""
    with smtplib.SMTP("smtp.gmail.com") as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=RECEIPT_EMAIL, msg=f"{message}")
