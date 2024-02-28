import requests
import calendar
from bs4 import BeautifulSoup
from datetime import datetime

month_names = [
    "Enero",
    "Febrero",
    "Marzo",
    "Abril",
    "Mayo",
    "Junio",
    "Julio",
    "Agosto",
    "Septiembre",
    "Octubre",
    "Noviembre",
    "Diciembre",
]


def splitDates(reference_date):
    date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    dateSplited = {"year": year, "month": month, "day": day}
    return dateSplited


def number_to_month(month):
    return month_names[month - 1]


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


def get_soup_by_month(url, month_number):
    list_of_links = []
    print(month_number)
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    if month_number < 13:
        for name_month in range(month_number + 1, 13):
            name = number_to_month(name_month)
            links_with_gestion_2023 = soup.find_all(
                "a", string=lambda text: name in str(text)
            )
            for link in links_with_gestion_2023:
                link_url = link.get("href")
                list_of_links.append(link_url)

    return list_of_links


# URL de la página web
url = "https://www.aduana.gob.bo/aduana7/content/bolet%C3%ADn-de-recaudaciones-0"
input_date = "2023-10-31"
date_split = splitDates(input_date)
management_year = f"Gestión {date_split['year']}"
link_url = get_soup_by_year(url, management_year)
print(link_url)
list_of_links = get_soup_by_month(link_url, date_split["month"])
print(list_of_links)
