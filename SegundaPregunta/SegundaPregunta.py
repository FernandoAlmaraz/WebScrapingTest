from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
from collections import defaultdict
import PyPDF2

months = [
    "ENERO",
    "FEBRERO",
    "MARZO",
    "ABRIL",
    "MAYO",
    "JUNIO",
    "JULIO",
    "AGOSTO",
    "SEPTIEMBRE",
    "OCTUBRE",
    "NOVIEMBRE",
    "DICIEMBRE",
]


def split_dates(reference_date):
    date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    return {"year": year, "month": month, "day": day}


def number_to_month(month):
    return months[month - 1]


def find_mounth(newstellers, month):
    index_reference_month = -1
    for newsteller in newstellers:
        if month in newsteller:
            index_reference_month = months.index(month)
            break

    if index_reference_month != -1:
        return months[index_reference_month + 1 :]
    else:
        return None


def clean_list(list):

    return [
        element
        for element in list
        if element.strip() and any(month in element.upper() for month in months)
    ]


def get_soup_by_year(url, texto_to_find):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    links_with_gestion_2023 = soup.find_all(
        "a", string=lambda text: texto_to_find in str(text)
    )
    for link in links_with_gestion_2023:
        link_url = link.get("href")

    if link_url.startswith("http"):
        target_url = link_url
    else:
        target_url = "https://www.aduana.gob.bo" + link_url

    return target_url


url = "https://www.bcb.gob.bo/?q=pub_boletin-mensual"
reference_date = "2023-09-30"
date_split = split_dates(reference_date)
month = number_to_month(date_split["month"])


driver_path = "C:\\Users\\Ferchex\\Downloads\\chromedriver-win64\chromedriver.exe"
options = Options()
options.add_argument("--ignore-certificate-errors")
service = Service(driver_path)
driver = webdriver.Chrome(service=service, options=options)
# driver.maximize_window()
driver.get(url)

data = []
date_element = driver.find_elements(
    By.XPATH,
    "//span",
)
for date_text in date_element:
    data.append(date_text.text)


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


def filter_links_by_month(results, months):
    filtered_results = []
    for result in results:
        for month in months:
            if month.upper() in result["date"].upper():
                filtered_results.append(result)
                break
    return filtered_results


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


def get_names_in_pdf_with_link(filtered_links):
    links_to_downloads = []
    for link_info in filtered_links:
        base_link = link_info["link"]
        response = requests.get(base_link)
        content_str = response.content.decode("utf-8", errors="replace")
        lines = content_str.split("\r\n")
        for line in lines:
            if "/URI(" in line:
                start_index = line.find("/URI(") + len("/URI(")
                end_index = line.find(")", start_index)
                link = line[start_index:end_index]
                base_url = base_link.split("/")[0:8]
                complete_url = "/".join(base_url)
                links_to_downloads.append(f"{complete_url}/{link}")
    return links_to_downloads


def remove_duplicates(urls):
    unique_urls = defaultdict(list)

    for url in urls:
        number = url.split("/")[-1].split(".")[0]
        file_type = url.split(".")[-1]
        key = f"{number}.{file_type}"
        unique_urls[key].append(url)

    unique_list = [urls[0] for urls in unique_urls.values()]

    return unique_list


def read_pdf(file_path):

    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


list_cleaned = clean_list(data)
list_of_months = find_mounth(list_cleaned, month)
list_of_downloand_links = get_links_and_dates(url)
filtered_links = filter_links_by_month(list_of_downloand_links, list_of_months)
names = get_names_in_pdf_with_link(filtered_links)

unique_names = remove_duplicates(names)
download_folder = (
    "C:\\Users\\Ferchex\\Desktop\\WebScrapingTest\\SegundaPregunta\\Descargas"
)
os.makedirs(download_folder, exist_ok=True)

initial_files_name = download_files(filtered_links, download_folder)
# ya tengo de donde sacar los nombres para los links
for file in initial_files_name:
    print(file)

# saco los nombres y los asigno a los links que son: "names"
time.sleep(4)
