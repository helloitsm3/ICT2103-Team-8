"""

Web Scrapping Library
General purpose library for any web scraping functions

"""

import requests
import re
from bs4 import BeautifulSoup

# list of urls to be scrapped
cathayUrl = "https://www.cathaycineplexes.com.sg/movies/"


"""
Function to replace a list of strings in a string
"""


def multiple_replace(dict, text):
    regex = re.compile("(%s)" % "|".join(map(re.escape, dict.keys())))
    return regex.sub(lambda mo: dict[mo.string[mo.start() : mo.end()]], text)


"""
Function to scrape the cathay movie website
Returns a list of movie names in a 2d array, no data.
"""


def cathay_scraper():

    movieList = []
    # list of all ratings, to remove from the scrapped movie title
    ageTag = {"NC16": "", "PG13": "", "M18": "", "TBA": "", "PG": "", "(Mandarin)": ""}

    # download the page using bs4
    page = requests.get(cathayUrl)
    soup = BeautifulSoup(page.content, "html.parser")

    # counter to help skip every other iteration, because of duplicates
    counter = 0

    # select all the movie titles, which are under the h3 tags
    for t in soup.find_all("h3", text=True):
        if counter == 1:
            counter = 0
            continue
        else:
            counter = 1
        # remove unneccsaryy characters with re
        title = re.sub("[*]", "", t.text)
        movieList.append(multiple_replace(ageTag, title))

    return movieList
