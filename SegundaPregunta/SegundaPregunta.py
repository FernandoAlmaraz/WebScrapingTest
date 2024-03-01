from datetime import datetime
import requests
from bs4 import BeautifulSoup
import os
from collections import defaultdict
import PyPDF2
import re

script_directory = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(script_directory, "Descargas")
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


def get_names_in_pdf_with_link(base_link):
    links_to_downloads = []
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


def find_months_in_span(url):
    data = []
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    date_element = soup.find_all("span")
    for date_text in date_element:
        data.append(date_text.text)
    return data


def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


def split_and_order_names(pdf_text):
    lines = pdf_text.split("\n")
    result = {}
    for line in lines:
        if re.match(r"^\d", line):
            number, rest = re.match(r"^(\d+)(.*)", line).groups()
            result[number] = rest.strip()
        else:
            result[line] = line
    return result


def process_links_with_names(links, names):
    result = {}
    for link in links:
        filename = os.path.basename(link)
        file_name_no_ext, extension = os.path.splitext(filename)
        number = "".join(filter(str.isdigit, file_name_no_ext))
        name = names.get(str(number), "")
        if not name:
            name = file_name_no_ext
        new_name = f"{name} {extension}"
        result[link] = new_name.capitalize()
    return result


def titles_of_initial_pdf(initial_files_path):
    result = {}
    for path in initial_files_path:
        pdf_text = read_pdf(path)
        splited_names = split_and_order_names(pdf_text)
        result.update(splited_names)
    return result


def save_dict_to_txt(dictionary, filename):
    with open(filename, "w") as file:
        for key, value in dictionary.items():
            file.write(f"{value}\n{key}\n")


def distroy_pdf_files(download_folder):
    for filename in os.listdir(download_folder):
        if filename.endswith(".pdf"):
            file_path = os.path.join(download_folder, filename)
            os.remove(file_path)


###################################################
# Acá puede configurar la fecha para que sea dinámica la busqueda.
reference_date = "2023-09-30"
#
url = "https://www.bcb.gob.bo/?q=pub_boletin-mensual"
date_split = split_dates(reference_date)
month = number_to_month(date_split["month"])

data = find_months_in_span(url)
list_cleaned = clean_list(data)
list_of_months = find_mounth(list_cleaned, month)
list_of_downloand_links = get_links_and_dates(url)
filtered_links = filter_links_by_month(list_of_downloand_links, list_of_months)
os.makedirs(download_folder, exist_ok=True)
initial_files_name = download_files(filtered_links, download_folder)
final_result = {}
test_procesed = titles_of_initial_pdf(initial_files_name)
filename = f"{download_folder}/links_and_names.txt"
for link in filtered_links:
    all_links_uri = get_names_in_pdf_with_link(link["link"])
    full_link_unique = remove_duplicates(all_links_uri)

    final_result = process_links_with_names(full_link_unique, test_procesed)
    save_dict_to_txt(final_result, filename)
    distroy_pdf_files(download_folder)
