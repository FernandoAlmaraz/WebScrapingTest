import PyPDF2
import requests
from bs4 import BeautifulSoup

url = "https://www.bcb.gob.bo/webdocs/publicacionesbcb/2024/01/18/%C3%8Dndice%20Boletin%20Mensual%20Octubre%202023.pdf"

import subprocess
import requests
import tempfile
import os

import pdfplumber
from bs4 import BeautifulSoup

import PyPDF2


# que lea cada linea y lo acomode segun los numero boletin tiene que repetirse
# los demas que no tienen numero que sean subclave
def read_pdf(file_path):
    text = ""
    with open(file_path, "rb") as file:
        reader = PyPDF2.PdfReader(file)
        num_pages = len(reader.pages)
        for page_num in range(num_pages):
            page = reader.pages[page_num]
            text += page.extract_text()
    return text


pdf_path = "C:\\Users\\Ferchex\\Desktop\\WebScrapingTest\\SegundaPregunta\\Descargas\\%C3%8Dndice%20Boletin%20Mensual%20Noviembre%202022.pdf"

pdf_text = read_pdf(pdf_path)
lines = pdf_text.strip().split("\n")
data = {}

current_key = "BOLETÍN COMPLETO"
data[current_key] = ""
for line in lines:
    if line.strip():  # Verificar si la línea no está vacía
        elements = line.split(maxsplit=1)
        if len(elements) == 2:  # Verificar si hay suficientes elementos
            number, value = elements
            data[number] = value.strip()
        else:
            data[current_key] += " " + line.strip()


print(data)
# print(pdf_text)
