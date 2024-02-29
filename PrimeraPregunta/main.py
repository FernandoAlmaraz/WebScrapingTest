from link_stractor import LinkExtractor
from datetime import datetime
from date_helper import DateHelper


class Main:
    def __init__(self, url, input_date):
        self.url = url
        self.input_date = input_date
        self.link_extractor = LinkExtractor(self.url)
        self.date_split = self.link_extractor.date_helper.split_dates(self.input_date)

    def run(self):
        management_year = f"Gestión {self.date_split['year']}"
        link_url = self.link_extractor.from_year(management_year)
        list_of_links = self.link_extractor.from_month(
            self.date_split["month"], link_url
        )
        self.print_results(link_url, list_of_links)
        self.save_results(link_url, list_of_links)

    def save_results(self, link_url, list_of_links):
        month_name = self.link_extractor.date_helper.number_to_month(
            self.date_split["month"]
        )
        with open("results.txt", "w") as file:
            file.write(f"Link de Gestión {self.date_split['year']}: {link_url}\n")
            file.write(
                f"Links desde {month_name} {self.date_split['year']} en adelante:\n"
            )
            for link in list_of_links:
                file.write(f"{link}\n")

    def print_results(self, link_url, list_of_links):
        month_name = self.link_extractor.date_helper.number_to_month(
            self.date_split["month"]
        )
        print(
            f"Link de Gestión {self.date_split['year']}:",
            link_url,
        )
        print(
            f"Links desde {month_name} {self.date_split['year']} en adelante:",
            list_of_links,
        )


if __name__ == "__main__":
    url = "https://www.aduana.gob.bo/aduana7/content/bolet%C3%ADn-de-recaudaciones-0"
    input_date = "2019-1-30"
    main_instance = Main(url, input_date)
    main_instance.run()
