import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

# Obtener la ruta del script actual y establecer el directorio de descargas
script_path = os.path.dirname(os.path.abspath(__file__))
download_path = os.path.join(script_path, "Descargas")
os.makedirs(download_path, exist_ok=True)

# URL de la página web a hacer web scraping
url = "https://www.ine.gob.bo/index.php/estadisticas-economicas/hidrocarburos-mineria/mineria-cuadros-estadisticos/"

# Texto que se buscará en los enlaces
text_to_find = "Bolivia – Producción Nacional de Minerales por Tipo de Mineral según Año y Mes 1990 – 2023"

# Realizar la solicitud GET y analizar el contenido HTML
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")

# Encontrar todos los enlaces que contienen el texto especificado
links_with_text = soup.find_all("a", string=lambda text: text_to_find in str(text))


# Función para descargar y guardar un archivo desde una URL
def download_file(url, download_path):
    # Parsear la URL para obtener el nombre del archivo
    file_name = os.path.basename(urlparse(url).path + ".xlsx")
    file_name = file_name.replace(" ", "")
    # Ruta completa donde se guardará el archivo
    paht_file = os.path.join(download_path, file_name)

    # Realizar la solicitud GET para descargar el archivo
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa (código de estado 200)
    if response.status_code == 200:
        # Guardar el contenido del archivo en un archivo local
        with open(paht_file, "wb") as archivo:
            archivo.write(response.content)
        print(
            f"El archivo '{file_name}' se ha descargado correctamente en '{download_path}'."
        )
    else:
        print(
            f"Error al descargar el archivo. Código de estado: {response.status_code}"
        )


# Descargar y guardar cada archivo asociado a los enlaces encontrados
for link in links_with_text:
    link_url = link.get("href")
    download_file(link_url, download_path)
