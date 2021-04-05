from service.web_scraping import amz_price_verifier
from service.content import get_data
from service.notifications import send_email
user_data = get_data()

for idx in range(len(user_data.get("tracker"))):
    url_amz = user_data.get("tracker")[idx]['url']
    desired_price = float(user_data.get("tracker")[idx]['desiredPrice'])
    amz_price, product_title, amz_buy_url = amz_price_verifier(url_amz)
    if amz_price is not None:
        if desired_price >= amz_price:
            message = f"Subject:Amz Price Alert!\n\nThe product:{product_title}\nIs below your desired " \
                        f"price of: {desired_price}\nBuy it now for: {amz_price}\nURL:{amz_buy_url}"
            try:
                send_email(message)
                print("The code was successfully executed")
            except ValueError:
                message = f"Subject:Amz Price Alert!\n\nThe product that you are tracking\nIs below your desired " \
                          f"price of: {desired_price}\nBuy it now for: {amz_price}\nURL:{amz_buy_url}"
                send_email(message)
                print("There was a problem encoding the title")

    else:
        message = f"Subject:AMZ Tracker Issue!\n\nThere is a problem tracking the {url_amz}, verify the code"
        send_email(message)
        print("The code was not successfully executed")
