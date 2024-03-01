import os
import requests
from bs4 import BeautifulSoup


class Download:
    @staticmethod
    def download_files(links, download_folder):
        filepaths = []
        for link in links:
            response = requests.get(link["link"])
            filename = link["link"].split("/")[-1]
            filepath = os.path.join(download_folder, filename)
            with open(filepath, "wb") as file:
                file.write(response.content)
            filepaths.append(filepath)
        return filepaths

    @staticmethod
    def get_links_and_dates(url):
        data = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        divs = soup.find_all("div", class_="views-row")
        for div in divs:
            span_title = div.find("span", class_="bcb_title")
            if span_title:
                date = span_title.text.split()[-2]
                link = div.find("a").get("href")
                data.append({"date": date, "link": link})

        return data

    @staticmethod
    def filter_links_by_month(results, months):
        filtered_results = []
        for result in results:
            for month in months:
                if month.upper() in result["date"].upper():
                    filtered_results.append(result)
                    break
        return filtered_results

    @staticmethod
    def find_months_in_span(url):
        data = []
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        date_element = soup.find_all("span")
        for date_text in date_element:
            data.append(date_text.text)
        return data

    @staticmethod
    def destroy_pdf_files(download_folder):
        for filename in os.listdir(download_folder):
            if filename.endswith(".pdf"):
                file_path = os.path.join(download_folder, filename)
                os.remove(file_path)
