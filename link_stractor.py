from web_scraper import WebScraper
from date_helper import DateHelper


class LinkExtractor:
    def __init__(self, url):
        self.url = url
        self.web_scraper = WebScraper(self.url)
        self.date_helper = DateHelper()

    def from_year(self, year_text):
        soup = self.web_scraper.get_soup()
        links_with_year = soup.find_all("a", string=lambda text: year_text in str(text))
        for link in links_with_year:
            link_url = link.get("href")
            if link_url.startswith("http"):
                return link_url
            else:
                return "https://www.aduana.gob.bo" + link_url

    def from_month(self, month_number, url):
        list_of_links = []
        soup = self.web_scraper.get_soup_by_url(url)
        for name_month in range(month_number + 1, 13):
            name = self.date_helper.number_to_month(name_month)
            links_with_month = soup.find_all("a", string=lambda text: name in str(text))
            for link in links_with_month:
                link_url = link.get("href")
                list_of_links.append(link_url)
        return list_of_links
