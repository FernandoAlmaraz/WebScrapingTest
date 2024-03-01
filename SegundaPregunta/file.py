import os
import PyPDF2
import re


class File:

    def titles_of_initial_pdf(initial_files_path):
        result = {}
        for path in initial_files_path:
            pdf_text = read_pdf(path)
            splited_names = split_and_order_names(pdf_text)
            result.update(splited_names)
        return result

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

    def save_dict_to_txt(dictionary, filename):
        with open(filename, "w") as file:
            for key, value in dictionary.items():
                file.write(f"{value}\n{key}\n")

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
