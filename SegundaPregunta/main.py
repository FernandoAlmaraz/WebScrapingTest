from datetime import datetime
import os

from file import File
from download import Download
from processing import Processing

script_directory = os.path.dirname(os.path.abspath(__file__))
download_folder = os.path.join(script_directory, "Descargas")


def main():
    # Definir la fecha de referencia
    reference_date = "2023-09-30"
    url = "https://www.bcb.gob.bo/?q=pub_boletin-mensual"
    # Dividir la fecha en sus componentes
    date_split = Processing.split_dates(reference_date)
    month = Processing.number_to_month(date_split["month"])

    # Obtener los meses siguientes al de referencia
    data = Download.find_months_in_span(url)
    list_cleaned = Processing.clean_list(data)
    list_of_months = Processing.find_mounth(list_cleaned, month)
    list_of_downloads = Download.get_links_and_dates(url)
    filtered_links = Download.filter_links_by_month(list_of_downloads, list_of_months)

    # Crear el directorio de descargas si no existe
    os.makedirs(download_folder, exist_ok=True)

    # Descargar los archivos y obtener sus nombres
    initial_files_name = Download.download_files(filtered_links, download_folder)
    test_procesed = File.titles_of_initial_pdf(initial_files_name)

    # Procesar los enlaces y nombres de los archivos
    final_result = File.process_links_with_names(filtered_links, test_procesed)

    # Guardar los nombres de los archivos en un archivo de texto
    filename = os.path.join(download_folder, "links_and_names.txt")
    File.save_dict_to_txt(final_result, filename)

    # Eliminar los archivos PDF descargados
    Download.destroy_pdf_files(download_folder)


if __name__ == "__main__":
    main()
