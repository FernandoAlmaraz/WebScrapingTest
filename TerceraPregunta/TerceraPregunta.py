import re
import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import pandas as pd
from datetime import datetime

script_path = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(script_path, "Descargas")
os.makedirs(download_path, exist_ok=True)
months = [
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

url = "https://www.ine.gob.bo/index.php/estadisticas-economicas/hidrocarburos-mineria/mineria-cuadros-estadisticos/"

text_to_find = "Bolivia – Producción Nacional de Minerales por Tipo de Mineral según Año y Mes 1990 – 2023"

response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

links_with_text = soup.find_all("a", string=lambda text: text_to_find in str(text))


def split_dates(reference_date):
    date_obj = datetime.strptime(reference_date, "%Y-%m-%d")
    year = date_obj.year
    month = date_obj.month
    day = date_obj.day
    return {"year": year, "month": month, "day": day}


def number_to_month(month):
    return months[month - 1]


def check_older_months(values, month_reference):

    mes_index = months.index(month_reference)
    return [
        months.index(curent_month) > mes_index
        for curent_month in values
        if curent_month in months
    ]


def download_file(url, download_path, text_to_find):
    text_to_find = text_to_find.replace(" ", "")
    file_name = text_to_find + ".xlsx"
    paht_file = os.path.join(download_path, file_name)
    response = requests.get(url)
    if response.status_code == 200:
        with open(paht_file, "wb") as archivo:
            archivo.write(response.content)
        print(
            f"El archivo '{file_name}' se ha descargado correctamente en '{download_path}'."
        )
    else:
        print(
            f"Error al descargar el archivo. Código de estado: {response.status_code}"
        )


for link in links_with_text:
    link_url = link.get("href")
    download_file(link_url, download_path, text_to_find)

text_to_find = text_to_find.replace(" ", "")
file_name = text_to_find + ".xlsx"
full_path_file = download_path + "/" + file_name

df = pd.read_excel(full_path_file, header=None, skiprows=2)
df = df.drop(columns=[0])
date_data = {}
date_data["fechas"] = df[1]
data_df = pd.DataFrame(date_data)


date_to_compare = "2023-10-31"
date_splited = split_dates(date_to_compare)
date_obj = number_to_month(date_splited["month"])
year_to_find = str(date_splited["year"]) + "(p)"
year_to_find = year_to_find
year_index = date_data["fechas"].tolist().index(year_to_find)
result = date_data["fechas"].tolist()[year_index:]
old_months = check_older_months(result, date_obj)
print(old_months)
