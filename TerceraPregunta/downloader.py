import os
import requests


class Downloader:
    def __init__(self, download_path):
        self.download_path = download_path

    def download_file(self, url, file_name):
        response = requests.get(url)
        if response.status_code == 200:
            file_path = os.path.join(self.download_path, file_name)
            with open(file_path, "wb") as file:
                file.write(response.content)
            print(
                f"File '{file_name}' downloaded successfully at '{self.download_path}'."
            )
        else:
            print(f"Error downloading the file. Status code: {response.status_code}")
