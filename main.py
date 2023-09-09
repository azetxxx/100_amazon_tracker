from bs4 import BeautifulSoup
# from email.mime.text import MIMEText
import lxml
import os
import requests
import smtplib


SENDER_EMAIL = "a.zinovev@hotmail.com"
SENDER_PASS = os.environ.get("SEND_PASS")
RECEIVER_EMAIL = "a.zinovev@hotmail.com"


# Scrapping of the amazon item price
def get_item_price(item_url):
    response = requests.get(item_url,
                            headers={
                                "Accept-Language":"de-DE,de;q=0.9,en-US;q=0.8,en;q=0.7,la;q=0.6,ru;q=0.5",
                                "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"})

    soup = BeautifulSoup(response.text, "lxml")
    item_price = soup.find(class_="a-price-whole")
    price = int(item_price.text[:-1].replace(".", ""))
    title = soup.title.text
    print(f"\n🏷️ {title}\n")
    print(f"💰 Current price is {price} euros.\n")
    return title, price


# Sending alarm email
def send_alarm_email(item_title, item_price, item_url, target_price):
        subject = f"=?utf-8?Q?=F0=9F=9A=A8?= AMAZON PRICE ALERT"
        # subject = f"🚨 AMAZON PRICE ALERT"
        email_text = f"🏷️ {item_title}\n\n\
            🎯 You set the Target Price {target_price} euro.\n\
            💰 The CURRENT PRICE is {item_price} euro!\n\
            -------------------------------------\n\
            🏃🏻‍♂️ Order now: {item_url}"

        # msg = MIMEText(email_text, 'plain', 'utf-8')
        # msg['Subject'] = subject

        with smtplib.SMTP("smtp-mail.outlook.com", 587) as connection:
            connection.starttls()
            connection.login(user=SENDER_EMAIL, password=SENDER_PASS)
            connection.sendmail(from_addr=SENDER_EMAIL,
                                to_addrs=RECEIVER_EMAIL,
                                msg=f"Subject:{subject}\n\n{email_text}".encode("utf-8")
                                # msg=msg.as_string()
                                )
        print(f"✅ Alarm email successfully sent!\n")


def main():
    item_url = 'https://www.amazon.de/Bosch-Tischbohrmaschine-PBD-Parallelanschlag-Schnellspannklemmen/dp/B005OQEK9W/ref=sr_1_3?crid=ZJWR61A3JFWG&keywords=bosch%2Btischbohrmaschine&qid=1694291712&sprefix=bosch%2Btisch%2Caps%2C110&sr=8-3&ufe=app_do%3Aamzn1.fos.8809de54-1c88-4fed-a3b8-b9f4f10823d1&th=1'
    target_price = 390

    item_title, current_price = get_item_price(item_url)

    if target_price >= current_price:
        send_alarm_email(item_title, current_price, item_url, target_price)


if __name__ == '__main__':
    main()
