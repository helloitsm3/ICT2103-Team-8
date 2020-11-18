import os
import re
import json
import pymongo
import psycopg2
import mysql.connector

from pymongo import MongoClient, ReturnDocument
from scripts.commands import *
from mysql.connector.errors import IntegrityError


# POSTGRESQL VAR
DB_POSTGRESQL_NAME = os.getenv("DB_POSTGRESQL_NAME")
DB_POSTGRESQL_HOST = os.getenv("DB_POSTGRESQL_HOST")
DB_POSTGRESQL_USER = os.getenv("DB_POSTGRESQL_USER")
DB_POSTGRESQL_PASS = os.getenv("DB_POSTGRESQL_PASS")

# MYSQL VAR
DB_MYSQL_NAME = os.getenv("DB_MYSQL_NAME")
DB_MYSQL_HOST = os.getenv("DB_MYSQL_HOST")
DB_MYSQL_USER = os.getenv("DB_MYSQL_USER")
DB_MYSQL_PASS = os.getenv("DB_MYSQL_PASS")

# LOCAL MYSQL VAR
DB_LOCAL_MYSQL_NAME = os.getenv("DB_LOCAL_MYSQL_NAME")
DB_LOCAL_MYSQL_HOST = os.getenv("DB_LOCAL_MYSQL_HOST")
DB_LOCAL_MYSQL_USER = os.getenv("DB_LOCAL_MYSQL_USER")
DB_LOCAL_MYSQL_PASS = os.getenv("DB_LOCAL_MYSQL_PASS")

# MONGODB VAR
DB_MONGO_URL = os.getenv("DB_MONGO_URL")


class Database:
    def __init__(self):
        config_file = open("static/config.json")
        config_data = json.load(config_file)
        CURRENT_DATABASE = config_data["current_database"]
        self.database = CURRENT_DATABASE

        if self.database == "postgresql":
            try:
                self.db_conn = psycopg2.connect(
                    """
                    dbname={0}
                    host={1}
                    user={2}
                    password={3}
                    sslmode=require
                    """.format(
                        DB_POSTGRESQL_NAME,
                        DB_POSTGRESQL_HOST,
                        DB_POSTGRESQL_USER,
                        DB_POSTGRESQL_PASS,
                    )
                )
                self.db_cursor = self.db_conn.cursor()
                print("Successfully connected to PostgreSQL Database")
            except:
                print("Failed to connect to PostgreSQL AWS Database")

        elif "mysql" in self.database:
            try:
                self.db_conn = mysql.connector.connect(
                    host=DB_MYSQL_HOST,
                    user=DB_MYSQL_USER,
                    passwd=DB_MYSQL_PASS,
                    database=DB_MYSQL_NAME,
                )

                self.db_conn.autocommit = True
                self.db_cursor = self.db_conn.cursor()
                print("Successfully connected to MySQL Alicloud Database")
            except mysql.connector.errors.InterfaceError:
                try:
                    self.db_conn = mysql.connector.connect(
                        host=DB_LOCAL_MYSQL_HOST,
                        user=DB_LOCAL_MYSQL_USER,
                        passwd=DB_LOCAL_MYSQL_PASS,
                        database=DB_LOCAL_MYSQL_NAME,
                    )

                    self.db_conn.autocommit = True
                    self.db_cursor = self.db_conn.cursor()
                    print("Successfully connected to MySQL Local Database")
                except:
                    print("Failed to connect to MySQL Database")

        elif "mongo" in self.database:
            try:
                self.db_conn = MongoClient(DB_MONGO_URL)
                print("Successfully connected to Mongo Database")
            except:
                print("Failed to connect to MongoDB")

    def getDBCursor(self):
        if "mongo" not in self.database:
            return self.db_cursor
        else:
            return ""

    # Get DB Connection
    def getDBConn(self):
        return self.db_conn

    def getDB(self):
        return self.database

    # Insert a movie into DB
    # TODO ADD "NOT EXIST" clause so that it doesn't insert duplicate movie
    def insertMovie(self, runtime, poster, plot, title, release):
        if "mongo" not in self.database:
            try:
                data_movie = ("4", runtime, poster, plot, title, release)
                self.db_cursor.execute(INSERT_MOVIE, data_movie)
            except IntegrityError:
                print("Failed to insert Movie: {0} as it already exist".format(title))
        else:
            # FOR ALL MONGO QUERIES
            try:
                self.db_conn["moviedb"]["movies"].insert_one(
                    {
                        "_id": {"title": title, "release": release},
                        "title": title,
                        "run_time": runtime,
                        "poster": poster,
                        "release": release,
                        "plot": plot,
                        "reviews": [],
                    }
                )
            except pymongo.errors.DuplicateKeyError:
                print("Fail to insert. Movie: {0} already exists".format(title))

    # Select a movie from db using poster url
    def fetchMovie(self, url):
        if "mongo" not in self.database:
            self.db_cursor.execute(FETCH_MOVIE, (url,))
            movie_data = self.db_cursor.fetchall()
            return movie_data

    def fetchMovieByName(self, name):
        filtered_name = name.replace("-", " ")
        if "mongo" not in self.database:
            self.db_cursor.execute(FETCH_MOVIE_BY_NAME, (filtered_name,))
            movie_data = self.db_cursor.fetchall()

            return movie_data

        else:
            # FOR ALL MONGO QUERIES
            # FETCHING FROM MONGO DB
            return self.db_conn["moviedb"]["movies"].find_one(
                {"title": re.compile("^" + filtered_name + "$", re.IGNORECASE)}
            )

    def cleanConnection(self):
        if "mongo" not in self.database:
            self.db_cursor.close()
            self.db_conn.close()

    # Function to create all necessary tables
    def initMySQLTable(self):
        try:
            # MYSQL USER TABLE
            self.db_cursor.execute(CREATE_USER_TBL)

            # MYSQL DIRECTOR TABLE
            self.db_cursor.execute(CREATE_DIRECTOR_TBL)

            # MYSQL MOVIE TABLE
            self.db_cursor.execute(CREATE_MOVIE_TBL)

            # MYSQL REVIEW TABLE
            self.db_cursor.execute(CREATE_REVIEW_TBL)

            # MYSQL MOVIELIST TABLE
            self.db_cursor.execute(CREATE_MOVIE_LIST_TBL)

            # MYSQL TIMESLOT TABLE
            self.db_cursor.execute(CREATE_TIMESLOT_TBL)

            # MYSQL SHOWTIME TABLE
            self.db_cursor.execute(CREATE_SHOWTIME_TBL)

            print("Successfully Created Tables")
        except AttributeError:
            print(
                "Failed to get DB Cursor. Are you trying to use cursor when querying mongodb? Try switch to PostgreSQL or MySQL"
            )

    def initMongoDB(self, **kwargs):
        if "mongo" in self.database:
            collection = self.db_conn["moviedb"]["movies"]

            # Created an Index for title so that it is much faster when returning queries
            collection.create_index("title")

    # Function to insert reviews
    def userSubmitReview(self, author_id, movie_id, points, review):
        if "mongo" not in self.database:
            self.db_cursor.execute(
                INSERT_REVIEW,
                (
                    author_id,
                    movie_id,
                    points,
                    review,
                ),
            )
        else:
            # Returns movie title if it's using mongodb
            data = self.db_conn["moviedb"]["movies"].find_one_and_update(
                {"title": movie_id},
                {
                    "$push": {
                        "reviews": {
                            "author": author_id,
                            "ratings": float(points),
                            "review": review,
                        }
                    }
                },
                return_document=ReturnDocument.AFTER,
            )

    # fetch top 10 movies
    def fetchTopTenMovieName(self):
        if "mongo" not in self.database:
            self.db_cursor.execute(FETCH_TOP_TEN_MOVIE_NAME)
            movie_top10_name = self.db_cursor.fetchall()
            return movie_top10_name
        else:
            # FETCHING FROM MONGO DB
            results = []
            queryStatement = (
                self.db_conn["moviedb"]["movies"]
                .find({}, {"title": 1, "_id": 0})
                .limit(10)
                .sort("title", -1)
            )
            for row in queryStatement:
                resultRow = []
                resultRow.append(row["title"])
                results.append(resultRow)
            print(results)
            return results

    # fetch from movie title search
    def fetchFromMovieSearch(self, serchTerm):
        if "mongo" not in self.database:
            self.db_cursor.execute(FETCH_FROM_MOVIE_SEARCH, ("%" + serchTerm + "%",))
            search_results = self.db_cursor.fetchall()
            self.db_cursor.close()
            self.db_conn.close()
            return search_results
        else:
            results = []
            # query based on searchTerm aka sql LIKE
            queryStatement = (
                self.db_conn["moviedb"]["movies"]
                .find(
                    {"title": {"$regex": serchTerm, "$options": "i"}},
                    {
                        "_id": 0,
                        "poster": 1,
                        "title": 1,
                        "run_time": 1,
                        "reviews": 1,
                    },
                )
                .sort("title", -1)
            )

            for row in queryStatement:
                rating = 0
                # for each movie, average the reviews rating
                pipeline = [
                    {"$match": {"title": row["title"]}},
                    {"$unwind": "$reviews"},
                    {
                        "$group": {
                            "_id": "$title",
                            "ratings_avg": {"$avg": "$reviews.ratings"},
                        }
                    },
                ]

                data = self.db_conn["moviedb"]["movies"].aggregate(pipeline)

                # get the rating from data object
                for i in data:
                    rating = i["ratings_avg"]

                # rearrange column to be same arrange as sql query result
                resultRow = (
                    row["poster"],
                    row["title"],
                    None,
                    row["run_time"],
                    round(rating, 2),
                )
                results.append(resultRow)

            results.sort(key=lambda x: x[4], reverse=True)
            return results

    def getData(self, key, *args):
        if "mongo" not in self.database:
            if len(args) <= 0:
                self.db_cursor.execute(key)
                data = self.db_cursor.fetchall()

                return data

            self.db_cursor.execute(key, args)
            data = self.db_cursor.fetchall()
            return data

    def fetchMovieReviews(self, moviename):
        if "mongo" in self.database:
            # $unwind - Deconstruct the value in the array to be used as variables
            # $group  - Group the document by ID
            # $push   - Preserves the original array by returning an array of all it's values

            filtered_name = moviename.replace("-", " ")
            filter_query = re.compile("^" + filtered_name + "$", re.IGNORECASE)

            pipeline = [
                {"$unwind": "$reviews"},
                {"$match": {"title": filter_query}},
                {
                    "$group": {
                        "_id": "$title",
                        "ratings": {"$push": "$reviews.ratings"},
                        "ratings_avg": {"$avg": "$reviews.ratings"},
                    },
                },
                {"$addFields": {"ratings_rounded": {"$round": ["$ratings_avg", 2]}}},
            ]

            data = self.db_conn["moviedb"]["movies"].aggregate(pipeline)

            for i in data:
                return i
