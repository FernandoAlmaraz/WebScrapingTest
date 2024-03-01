import PyPDF2

import re

url = "https://www.bcb.gob.bo/webdocs/publicacionesbcb/2024/01/18/%C3%8Dndice%20Boletin%20Mensual%20Octubre%202023.pdf"


pdf_path = "C:\\Users\\Ferchex\\Desktop\\WebScrapingTest\\SegundaPregunta\\Descargas\\%C3%8Dndice%20Boletin%20Mensual%20Noviembre%202022.pdf"


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
        if re.match(r"^\d", line):  # Comprueba si la línea comienza con un número
            number, rest = re.match(
                r"^(\d+)(.*)", line
            ).groups()  # Separa el número del resto del texto
            result[number] = (
                rest.strip()
            )  # Almacena el número como clave y el resto del texto como valor (sin espacios en blanco al inicio o al final)
        else:
            result[line] = (
                line  # Almacena la línea tanto como clave como valor si no comienza con un número
            )
    return result


pdf_text = read_pdf(pdf_path)
resultado = split_and_order_names(pdf_text)
print(resultado)
# print(pdf_text)

# lines = pdf_text.strip().split("\n")


# print(data)
# print(pdf_text)
