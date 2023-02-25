import requests
from bs4 import BeautifulSoup


class Movie:
    def __init__(self, link):
        headers = {"Accept-Language": "en-US,en;q=0.5",
                   'User-Agent': 'Mozilla/5.0'}
        response = requests.get(link, headers=headers)
        self.soup = BeautifulSoup(response.text, 'html.parser')

    def get_name(self):
        return self.soup.select_one('h1').text + f' ({self.get_year()})'

    def get_year(self):
        return self.soup.select_one('.sc-f26752fb-1').text

    #  ipc-metadata-list-item__list-content baseAlt
    def get_directors(self):
        directors = []
        directors_raw = self.soup.select_one(
            '.ipc-inline-list.ipc-inline-list--show-dividers.ipc-inline-list--inline')
        try:
            directors_list = directors_raw.select('li')
            for director in directors_list:
                director_name = director.text
                directors.append(director_name)
            return directors
        except AttributeError:
            return

    def get_actors(self):
        actors_raw = self.soup.select(
            '.sc-bfec09a1-1')
        return [actor.text for actor in actors_raw]
