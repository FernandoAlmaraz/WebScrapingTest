import requests
from bs4 import BeautifulSoup


class WebScraper:
    def __init__(self, url):
        self.url = url

    def get_soup(self):
        response = requests.get(self.url)
        return BeautifulSoup(response.text, "html.parser")

    def get_soup_by_url(self, url):
        response = requests.get(url)
        return BeautifulSoup(response.text, "html.parser")
