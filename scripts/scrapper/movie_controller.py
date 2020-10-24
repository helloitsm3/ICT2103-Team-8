'''

Movie Controller

Functions to process and collect movie, and insert into database.

'''

import scripts.scrapper.movie_data_lib as movie_lib
import scripts.scrapper.scrapper_lib as scrapper_lib
from scripts.database import Database





'''
This function gets top 4 posters for the main page

'''
def getCathayMainPosters():
    images = []
    movielist = scrapper_lib.cathay_scraper()
    for i in movielist:
        movie = movie_lib.omdb_fetch(i)
        # if it fails, its probably because of the ":" character confusing the api
        if movie['Response'] == 'False':
            i = i.split(":", maxsplit=1)[0]
            movie = movie_lib.omdb_fetch(i)
        # if it still fails, just skip
        if movie['Response'] == 'False':
            continue
        # check if invalid poster
        if movie['Poster'] != 'N/A':
            images.append(movie['Poster'])
        else:
            continue
        if len(images) == 4:
            break
    return images


'''
This function returns a list of movie poster urls, to populate the next screen.
Soon to update to a dictionary of movies.

This function also INSERTS MOVIES INTO THE DATABASE.

'''
def getCathayMovie():
    db = Database()
    movies = []
    movielist = scrapper_lib.cathay_scraper()
    for i in movielist:
        movie = movie_lib.omdb_fetch(i)
        # if it fails, its probably because of the ":" character confusing the api
        if movie['Response'] == 'False':
            i = i.split(":", maxsplit=1)[0]
            movie = movie_lib.omdb_fetch(i)
        # if it still fails, just skip
        if movie['Response'] == 'False':
            continue
        # check if invalid poster
        if movie['Poster'] != 'N/A':
            movies.append(movie['Poster'])
            plot = movie['Plot']
            print(plot, movie['Title'])
            db.insertMovie(movie['Runtime'], movie['Poster'], movie['Plot'], movie['Title'], movie['Released'])

        else:
            continue

    return movies