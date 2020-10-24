'''

Movie Database Library

Use this by calling the tmdb_fetch function and entering the search term
- i.e tmdb_fetch('mulan')
You can also enter the year
- tmdb_fetch_year('mulan',1998)

'''

import requests
import json

def omdb_fetch(name):
    response = requests.get('http://www.omdbapi.com/?t='+name+'&apikey=6a9110de&y=2020')
    moviejson = response.json()
    return moviejson

def tmdb_fetch(name):

    response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=bc08581718e425b5222363427b4b0a72&language=en-US&query='+name+'&page=1')
    moviejson = response.json()
    return moviejson['results']


def tmdb_fetch_year(name,year):

    response = requests.get('https://api.themoviedb.org/3/search/movie?api_key=bc08581718e425b5222363427b4b0a72&language=en-US&query='+name+'&page=1&year='+year)
    moviejson = response.json()
    return moviejson['results']

