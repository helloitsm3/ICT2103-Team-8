import os
import psycopg2
import mysql.connector
import pymongo

from pymongo import MongoClient


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

# MONGODB VAR
DB_MONGO_URL = os.getenv("DB_MONGO_URL")


class Database:
    def __init__(self, database="mysql"):
        try:
            self.database = database
            if database == "postgresql":
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

            elif database == "mysql":
                self.db_conn = mysql.connector.connect(
                    host=DB_MYSQL_HOST,
                    user=DB_MYSQL_USER,
                    passwd=DB_MYSQL_PASS,
                    database=DB_MYSQL_NAME,
                )

                self.db_conn.autocommit = True
                self.db_cursor = self.db_conn.cursor()
                print("Successfully connected to MySQL Database")

            elif "mongo" in database:
                self.db_conn = MongoClient(DB_MONGO_URL)
                print("Successfully connected to Mongo Database")
        except:
            print("Fail to connect to the database")

    def getDBCursor(self):
        if "mongo" not in self.database:
            return self.db_cursor

    # Get DB Connection
    def getDBConn(self):
        return self.db_conn

    # insert a movie into DB
    # TODO ADD "NOT EXIST" clause so that it doesn't insert duplicate movie
    def insertMovie(self, runtime, poster, plot, title, release):

        insert_movie = (
            "INSERT INTO Movie "
            "(ratings, run_time, poster_path, plot, title,release_date) "
            "VALUES (%s, %s, %s, %s, %s, %s)"
        )
        data_movie = ("4", runtime, poster, plot, title, release)

        self.db_cursor.execute(insert_movie, data_movie)

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

            # MYSQL REVIEW TABLE
            self.db_cursor.execute(
                """
                    CREATE TABLE IF NOT EXISTS Review (
                        review_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
                        author_id INT,                        
                        points DECIMAL(3, 2),
                        review VARCHAR(2500),
                        date_create DATETIME DEFAULT CURRENT_TIMESTAMP,                       
                        
                        CHECK (points > 0 AND points <= 5),
                        FOREIGN KEY (author_id) REFERENCES User(user_id) ON DELETE CASCADE
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
                        review_id INT,
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
                        FOREIGN KEY (review_id) REFERENCES Review(review_id),
                        FOREIGN KEY (director_id) REFERENCES Director(director_id)
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

            # self.db_cursor.execute(
            #     "SELECT DECODE('password1', 'secret') AS 'password' FROM 'User'"
            # )

            print("Successfully Created Tables")
        except AttributeError:
            print(
                "Failed to get DB Cursor. Are you trying to use cursor when querying mongodb? Try switch to PostgreSQL or MySQL"
            )

    # This function will return the current connection
    # of the database use this to interact with database query
    # def getCursor(self):
    #     return self.postgres_cursor

    # def getDBConnStatus(self):
    #     # DB STATUS CODE
    #     # Return status: 0 == connected
    #     # Return status: 1 == not connected
    #     return "Connected" if self.postgres_conn.closed == 0 else "Disconnected"

    def createUser(self, username, email, password, role):
        try:
            self.mysql_cursor.execute(
                "INSERT INTO User (username, email, password, role_id) VALUES ({0}, {1}, MD5({2}), {3})".format(
                    username, email, password, role
                )
            )
        except AttributeError:
            print(
                "Failed to get DB Cursor. Please make sure you're using a SQL Database"
            )

    def decodePassword(self, password):
        try:
            pass
        except AttributeError:
            print(
                "Failed to get DB Cursor. Please make sure you're using a SQL Database"
            )