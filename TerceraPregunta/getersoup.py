from bs4 import BeautifulSoup


class Parser:
    def __init__(self, html_content):
        self.soup = BeautifulSoup(html_content, "html.parser")

    def find_links_with_text(self, text_to_find):
        return self.soup.find_all("a", string=lambda text: text_to_find in str(text))
