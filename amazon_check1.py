import requests
from bs4 import BeautifulSoup
import smtplib
import os

GMAIL_EMAIL = "pythonwithjamess@gmail.com"
GM_PW = os.environ.get("GM_PW")
INBOX = "jamieslinger@gmail.com"
APP_PW = os.environ.get("APP_PW")
PRODUCT_URL = "https://www.amazon.co.uk/dp/B07DJ25QNT"
TARGET_PRICE = 13.0


def send_email_alert(price, name, link):
    with smtplib.SMTP("smtp.gmail.com") as con:
        con.starttls()
        con.login(user=GMAIL_EMAIL, password=APP_PW)
        con.sendmail(from_addr=GMAIL_EMAIL,
                     to_addrs=INBOX,
                     msg=f"Subject: Amazon Low Price Alert!"
                         f"\nHey James,"
                         f"\n\nAmazon Low Price Alert!"
                         f"\n\nProduct: {name}"
                         f"\n\nPrice: £{price}"
                         f"\n\nLink: {link}".encode("utf-8")
                     )


headers = {
    "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36",
    "referer": "https://google.co.uk",
}

product_data = requests.get(url=PRODUCT_URL, headers=headers)
data = product_data.text

bs = BeautifulSoup(data, "lxml")
price_data = bs.find(name="span", id="sns-base-price")
item_price = str(price_data.contents[0])
s_price = float(item_price.strip(" £"))
product_name = bs.find(name="span", id="productTitle").getText()
s_name = product_name.strip()

if s_price < TARGET_PRICE:
    send_email_alert(s_price, s_name, PRODUCT_URL)
    print("Sending email")
else:
    print("Too expensive!")
