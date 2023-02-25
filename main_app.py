import requests
import os
import shutil
import datetime
from bs4 import BeautifulSoup
from decouple import config
from classes import Movie
from openpyxl import Workbook


FIRST_ENTRY = config('FIRST_ENTRY')
BASE_LINK = 'https://www.imdb.com/'


def get_all_links():
    all_links = []
    ENTRY_LINK = FIRST_ENTRY
    try:
        while True:
            response = requests.get(ENTRY_LINK)
            soup = BeautifulSoup(response.text, 'html.parser')
            next_page = soup.select_one('.next-page')
            link = BASE_LINK + next_page['href']
            ENTRY_LINK = link
            raw_links = soup.select('.lister-item-header a')
            current_links = []
            for raw_link in raw_links:
                current_links.append(BASE_LINK + raw_link['href'])
            all_links.extend(current_links)
    except TypeError:
        print("No more pages")
    return all_links


def process_director(soup):
    raw_data = soup.select_one('.ipc-metadata-list__item')
    print(raw_data)


def create_movie_name(movie):
    return f"{movie.get_name()} [{movie.get_year()}]"


movie_links = get_all_links()
# movie_links = ['https://www.imdb.com/title/tt4176826/?ref_=wl_li_tt',
#                'https://www.imdb.com/title/tt1232829/?ref_=wl_li_tt',
#                'https://www.imdb.com/title/tt1663202/?ref_=nv_sr_srsg_0']
movie_number = 1
directors_list = {}
actors_list = {}
for link in movie_links:
    movie = Movie(link)
    movie_name = movie.get_name()
    print(f"{movie_number}/{len(movie_links)} -- {movie_name}")
    actors = movie.get_actors()
    for actor in actors:
        if actor in actors_list:
            actors_list[actor]['appearances'] += 1
            actors_list[actor]['movies'].append(movie_name)
        else:
            actors_list[actor] = {'appearances': 1,
                                  'movies': [movie_name]}
    movie_number += 1

    directors = movie.get_directors()
    for director in directors:
        if director in directors_list:
            directors_list[director]['appearances'] += 1
            directors_list[director]['movies'].append(movie_name)
        else:
            directors_list[director] = {
                'appearances': 1, 'movies': [movie_name]}


def get_year(movie):
    return movie[-5:-1:]


for actor in actors_list:
    actors_list[actor]['movies'].sort(key=get_year)

for director in directors_list:
    directors_list[director]['movies'].sort(key=get_year)

if os.path.exists('actors.xlsx'):
    ts = datetime.datetime.now().strftime('%d%m%Y%H%M')
    shutil.move('actors.xlsx', f'old/actors{ts}.xlsx')

wb = Workbook()
ws = wb.active
ws.title = 'Actors List'
ws.append(['Actor', 'Appearances', 'Movies'])
for (actor, values) in actors_list.items():
    ws.append([actor, values['appearances'], str(values['movies']
                                                 ).replace('[', '').replace(']', '').replace("'", '')])

ws2 = wb.create_sheet(title='Directors')
ws2.append(['Director', 'Appearances', 'Movies'])
for (director, values) in directors_list.items():
    ws2.append([director, values['appearances'], str(
        values['movies']).replace('[', '').replace(']', '').replace("'", '')])

wb.save('actors.xlsx')
