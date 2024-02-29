from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
import time
from datetime import datetime
import requests
import calendar
from bs4 import BeautifulSoup
from datetime import datetime

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
    # Encontrar el índice del mes de referencia en la lista de meses
    index_reference_month = months.index(month)
    # Obtener los meses siguientes al mes de referencia
    next_months = month[index_reference_month + 1 :]
    # Filtrar los boletines que contienen los meses siguientes
    next_newstellers = [
        newsteller
        for newsteller in newstellers
        if any(month in newsteller for month in next_months)
    ]
    return next_newstellers


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
driver.maximize_window()
driver.get(url)

data = []
date_element = driver.find_elements(
    By.XPATH,
    "//span",
)
for date_text in date_element:
    data.append(date_text.text)

# driver.find_element()

list_cleaned = clean_list(data)
print(list_cleaned)
print("lista limpia")
list_of_months = find_mounth(list_cleaned, month)
print(list_of_months)
print("lo de arriba era el")
time.sleep(50)
