from downloader import Downloader

from excelhandler import ExcelHandler
from helper import split_dates, number_to_month, check_older_months
from getersoup import Parser
import os
import requests

script_path = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(script_path, "Downloads")
os.makedirs(download_path, exist_ok=True)

url = "https://www.ine.gob.bo/index.php/estadisticas-economicas/hidrocarburos-mineria/mineria-cuadros-estadisticos/"
text_to_find = "Bolivia – Producción Nacional de Minerales por Tipo de Mineral según Año y Mes 1990 – 2023"

response = requests.get(url)
parser = Parser(response.text)
links_with_text = parser.find_links_with_text(text_to_find)

downloader = Downloader(download_path)
for link in links_with_text:
    link_url = link.get("href")
    downloader.download_file(link_url, text_to_find + ".xlsx")

excel_file_path = os.path.join(download_path, text_to_find + ".xlsx")
excel_handler = ExcelHandler(excel_file_path)

date_to_compare = "2023-10-31"
date_splited = split_dates(date_to_compare)
date_obj = number_to_month(date_splited["month"])
year_to_find = str(date_splited["year"]) + "(p)"
column_data = excel_handler.extract_column_data(1)
year_index = column_data.tolist().index(year_to_find)
result = column_data.tolist()[year_index:]
old_months = check_older_months(result, date_obj)
print(old_months)
