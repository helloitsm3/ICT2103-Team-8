import os
import re
import json
import pymongo
import psycopg2
import mysql.connector

from pymongo import MongoClient
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
                insert_movie = INSERT_MOVIE
                data_movie = ("4", runtime, poster, plot, title, release)

                self.db_cursor.execute(insert_movie, data_movie)
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
            fetch_movie = FETCH_MOVIE

            self.db_cursor.execute(fetch_movie, (url,))
            movie_data = self.db_cursor.fetchall()
            return movie_data

    def fetchMovieByName(self, name):
        filtered_name = name.replace("-", " ")
        if "mongo" not in self.database:
            fetch_movie = FETCH_MOVIE_BY_NAME

            self.db_cursor.execute(fetch_movie, (filtered_name,))
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
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS User (
                        user_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        movie_id INT,
                        username VARCHAR(50) NOT NULL UNIQUE,
                        email VARCHAR(50) NOT NULL,
                        password VARCHAR(255) NOT NULL,
                        role_id VARCHAR(25),
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                    )"""
            )

            # MYSQL DIRECTOR TABLE
            self.db_cursor.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS Director (
                        director_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        director_name VARCHAR(100) NOT NULL UNIQUE
                )"""
            )

            # MYSQL MOVIE TABLE
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Movie (
                        movie_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        ratings DECIMAL(3, 2),
                        genre VARCHAR(100),
                        country VARCHAR(100),
                        director_id INT,
                        run_time INT,
                        poster_path VARCHAR(250),
                        plot VARCHAR(2500),
                        title VARCHAR(150),
                        overview VARCHAR(2500),
                        original_language VARCHAR(25),
                        writers VARCHAR(1000),
                        casts VARCHAR(1000),
                        release_date DATETIME DEFAULT CURRENT_TIMESTAMP,

                        CHECK (ratings > 0 AND ratings <= 5),
                        FOREIGN KEY (director_id) REFERENCES Director(director_id),
                        CONSTRAINT UC_Movie UNIQUE (title, poster_path, release_date)
                )"""
            )

            # MYSQL REVIEW TABLE
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Review (
                        review_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        author_id INT,                        
                        movie_id INT,
                        points DECIMAL(3, 2),
                        review VARCHAR(2500),
                        date_create DATETIME DEFAULT CURRENT_TIMESTAMP,                       
                        
                        CHECK (points > 0 AND points <= 5),
                        FOREIGN KEY (author_id) REFERENCES User(user_id) ON DELETE CASCADE,
                        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE
                    )"""
            )

            # MYSQL MOVIELIST TABLE
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS MovieList (
                        user_id INT,
                        movie_id INT,

                        FOREIGN KEY (user_id) REFERENCES User(user_id),
                        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
                )"""
            )

            # MYSQL TIMESLOT TABLE
            self.db_cursor.execute(
                """ 
                    CREATE TABLE IF NOT EXISTS Timeslot (
                        showtime_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
                        slots VARCHAR(100),
                        date_showing DATETIME DEFAULT CURRENT_TIMESTAMP
                )"""
            )

            # MYSQL SHOWTIME TABLE
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Showtime (
                        movie_id INT,
                        showtime_id INT,

                        FOREIGN KEY (showtime_id) REFERENCES Timeslot(showtime_id),
                        FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
                )"""
            )

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
            submit_review = INSERT_REVIEW

            self.db_cursor.execute(
                submit_review,
                (
                    author_id,
                    movie_id,
                    points,
                    review,
                ),
            )

    # fetch top 10 movies
    def fetchTopTenMovieName(self):
        if "mongo" not in self.database:
            fetch_top10_movie_name = (
                "SELECT title FROM movie ORDER BY ratings DESC LIMIT 10"
            )

            self.db_cursor.execute(fetch_top10_movie_name)
            movie_top10_name = self.db_cursor.fetchall()
            return movie_top10_name

    # fetch from movie title search
    def fetchFromMovieSearch(self, serchTerm):
        if "mongo" not in self.database:
            fetch_from_movie_search = "SELECT M.poster_path, M.title, D.director_name, M.run_time, M.ratings \
                    FROM movie M LEFT JOIN director D ON M.director_id = D.director_id \
                        WHERE title LIKE %s ORDER BY ratings DESC"
            self.db_cursor.execute(fetch_from_movie_search, ("%" + serchTerm + "%",))
            search_results = self.db_cursor.fetchall()
            self.db_cursor.close()
            self.db_conn.close()
            return search_results

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
                    }
                },
            ]
            data = self.db_conn["moviedb"]["movies"].aggregate(pipeline)

            for i in data:
                return i
