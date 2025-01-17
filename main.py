from flask import Flask
from scripts.user import User

import scripts.scrapper.movie_data_lib as movie_lib
import scripts.scrapper.scrapper_lib as scrapper_lib

# ===== Routing =====
from routes.main_routes import data

import os

app = Flask(__name__)
app.secret_key = os.urandom(12)

# ===== Blueprints Registration =====
app.register_blueprint(data, url_prefix="/")


if __name__ == "__main__":
    app.run()

"""
#TESTING FUNCTIONS
movielist = scrapper_lib.cathay_scraper()
print("★★★Now Showing★★★")
for i in movielist:

    movie = movie_lib.tmdb_fetch(i)
    if movie:
        print("Movie Name: ",movie[0]['title'])
        print("Release Date: ",movie[0]['release_date'])
        print("Rating: ",movie[0]['vote_average'])
        print("Description: ",movie[0]['overview'])
        print("=========================================")
        print("=========================================")
"""
