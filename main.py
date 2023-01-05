import re
from time import sleep
from requests import Session
from selenium import webdriver
from bs4 import BeautifulSoup

DOWNLOAD_DIR = '../out/'
URL = 'https://european-union.europa.eu/news-and-events/press-releases_en?f%5B0%5D=aggregator_item_source%3A759&page={}'
JSON_url = ' https://ec.europa.eu/commission/presscorner/api/documents?reference={}/{}/{}&language=en&ts={}'
PAGES_BACK = 10
sess = Session()
HTML = """
    <head>
        <title>{}</title>
    </head>
    <body>
    {}
    </body>
       """

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-software-rasterizer')
chrome_options.add_argument('--headless')
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--window-size=1600,900')


def main():
    browser = webdriver.Chrome(options=chrome_options)
    counter = 0
    for page in range(PAGES_BACK):
        content = sess.get(URL.format(page)).content
        sleep(15)
        soup = BeautifulSoup(content, 'html.parser')
        h1_tags = soup.find_all('h1', {'class': 'ecl-content-block__title'})
        for h1_tag in h1_tags:
            article_url = h1_tag.find('a')['href']
            browser.get(article_url)
            sleep(15)
            cookies = browser.get_cookies()
            [name, year, id_number] = re.search('([A-Z]+).(\d{1,}).(\d{1,})', article_url).groups()
            key = cookies[0].get('expiry')
            JSON_content = sess.get(JSON_url.format(name, year, id_number, key, json_content=True)).json()
            current_html = HTML.format(JSON_content['docuLanguageResource']['title'],
                                       JSON_content['docuLanguageResource']['htmlContent'])
            with open(DOWNLOAD_DIR + f'{counter}.html', 'w', encoding='utf-8') as writer:
                writer.write(current_html)
                counter += 1
            if counter > 15:
                break


if __name__ == '__main__':
    main()
