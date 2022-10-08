import logging
import requests
from bs4 import BeautifulSoup
from flask import Flask

app = Flask(__name__)


@app.route('/api/v1/currency')
def bcv_web_scraping_currency():
    try:
        website = 'https://www.bcv.org.ve/'
        result = requests.get(website, verify=False)
        content = result.text
        soup = BeautifulSoup(content, 'lxml')
        box = soup.find('div', class_='view-tipo-de-cambio-oficial-del-bcv')

        currencys_price = box.findAll('strong')
        currencys_title = box.findAll('span')

        currencys_title.pop(0)
        currencys_title.pop(5)

        currencys_title_content = list()
        currencys_price_content = list()

        for n in currencys_title:
            currencys_title_content.append(n.text.strip())
        for j in currencys_price:
            currencys_price_content.append(j.text.strip())

        zip_iterator = zip(currencys_title_content, currencys_price_content)
        a_dictionary = dict(zip_iterator)

        return {'currency_lists': a_dictionary}

    except Exception as e:
        logging.exception(e)
        return {'status': 'error', 'currency_lists': ''}


if __name__ == '__main__':
    app.run()
