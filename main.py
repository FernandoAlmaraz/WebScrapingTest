from link_stractor import LinkExtractor
from datetime import datetime


class Main:
    def __init__(self, url, input_date):
        self.url = url
        self.input_date = input_date
        self.link_extractor = LinkExtractor(self.url)

    def run(self):
        date_split = self.link_extractor.date_helper.split_dates(self.input_date)
        management_year = f"Gestión {date_split['year']}"
        link_url = self.link_extractor.from_year(management_year)
        list_of_links = self.link_extractor.from_month(date_split["month"], link_url)
        self.print_results(link_url, list_of_links)

    def print_results(self, link_url, list_of_links):
        print("Link de Gestión 2023:", link_url)
        print("Links desde noviembre 2023 en adelante:", list_of_links)


if __name__ == "__main__":
    url = "https://www.aduana.gob.bo/aduana7/content/bolet%C3%ADn-de-recaudaciones-0"
    input_date = "2023-10-31"
    main_instance = Main(url, input_date)
    main_instance.run()
