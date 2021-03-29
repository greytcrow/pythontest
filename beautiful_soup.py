import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

import inquirer
from inquirer.themes import GreenPassion


def get_page_links(url):
    with urllib.request.urlopen(url) as response:
        webpage = response.read()
        soup = BeautifulSoup(webpage, 'html.parser')

        content = soup.find('div', class_="mw-page-container-inner")

        links = [link.get('href') for link in content.find_all('a')]
        return set(
            urllib.parse.unquote_plus(
                link.replace("/wiki/", "").replace("_", " "))
            for link in links
            if link is not None and
            link.startswith('/wiki/') and
            'fr.m.wikipedia.org' not in link and
            '/w/index.php' not in link and
            ':' not in link
        )


starting_point = urllib.request.urlopen(
    "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")
finish_line = urllib.request.urlopen(
    "https://fr.wikipedia.org/wiki/Sp%C3%A9cial:Page_au_hasard")

current_page = starting_point

while current_page.url != finish_line.url:
    URL_START = "https://fr.wikipedia.org/wiki/"
    print(urllib.parse.unquote_plus("vous etes sur la page " +
                                    current_page.url.replace(URL_START, "").replace("_", " ")))
    print(urllib.parse.unquote_plus("objectif : aller vers la page " +
                                    finish_line.url.replace(URL_START, "").replace("_", " ")))
    wiki_links = get_page_links(current_page.url)
    wiki = list(wiki_links)
    wiki.sort()
    questions = [
        inquirer.List('link',
                      choices=wiki,
                      ),
    ]
    answers = inquirer.prompt(questions, theme=GreenPassion())
    interm = (URL_START +
              answers['link'].replace(" ", "_"))
    current_page = urllib.request.urlopen(interm)
