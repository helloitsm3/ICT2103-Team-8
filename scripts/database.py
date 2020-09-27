import os
import psycopg2
import mysql.connector


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


class Database:
    def __init__(self):
        try:
            # self.postgres_conn = psycopg2.connect(
            #     """
            #     dbname={0}
            #     host={1}
            #     user={2}
            #     password={3}
            #     sslmode=require
            #     """.format(
            #         DB_POSTGRESQL_NAME,
            #         DB_POSTGRESQL_HOST,
            #         DB_POSTGRESQL_USER,
            #         DB_POSTGRESQL_PASS,
            #     )
            # )

            self.mysql_conn = mysql.connector.connect(
                host=DB_MYSQL_HOST,
                user=DB_MYSQL_USER,
                passwd=DB_MYSQL_PASS,
                database=DB_MYSQL_NAME,
            )
            self.mysql_cursor = self.mysql_conn.cursor()
            # self.postgres_cursor = self.postgres_conn.cursor()
        except:
            print("Fail to connect to the database")

    def getMySQLCursor(self):
        return self.mysql_cursor

    # Function to create all necessary tables
    def initMySQLTable(self):
        # MYSQL DIRECTOR TABLE
        self.mysql_cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS Director (
                    director_id int AUTO_INCREMENT,
                    movie_id int,

                    name VARCHAR(255) NOT NULL,

                    PRIMARY KEY (director_id)
            )"""
        )

        # MYSQL MOVIE TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Movie (
                    ratings int NOT NULL,
                    run_time int NOT NULL,

                    poster_path VARCHAR(255) NOT NULL,
                    writer VARCHAR(255) NOT NULL,
                    plot VARCHAR(255) NOT NULL,
                    country VARCHAR(255) NOT NULL,
                    genre VARCHAR(25) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    overview VARCHAR(255) NOT NULL,
                    original_language VARCHAR(255) NOT NULL,
                    release_date TIMESTAMP,

                    PRIMARY KEY (movie_id)
                )"""
        )

        # MYSQL GENRE TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Genre (
                    genre_id int AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL,

                    PRIMARY KEY (genre_id)
                )"""
        )

        # MYSQL REVIEW TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Review (
                    review_id int AUTO_INCREMENT,                    
                    points int NOT NULL,

                    review VARCHAR(255) NOT NULL,
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                    PRIMARY KEY (review_id)
            )"""
        )

        # MYSQL CAST TABLE
        self.mysql_cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS Cast (
                    cast_id int AUTO_INCREMENT,

                    full_name VARCHAR(255) NOT NULL,
                    description VARCHAR(255) NOT NULL,

                    PRIMARY KEY (cast_id)
            )"""
        )

        # MYSQL COUNTRY TABLE
        self.mysql_cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS Country (
                    country_id int AUTO_INCREMENT,
                    country_name VARCHAR(255) NOT NULL,

                    PRIMARY KEY (country_id)
            )"""
        )

        # MYSQL USER TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS User (
                    user_name VARCHAR(50), 
                    user_id int AUTO_INCREMENT,
                    user_password VARCHAR(100) NOT NULL,
                    movie_id int,
                    email VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (user_id),
                    FOREIGN KEY (movies_id) REFERENCES Movie(movie_id)
                )"""
        )

        # ALTER TABLE COMMAND
        self.mysql_cursor.execute(
            """
            ALTER TABLE Director ADD movie_id int AUTO_INCREMENT,
            ALTER TABLE Director ADD FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
            """
        )

        self.mysql_cursor.execute(
            """
                ALTER TABLE Movie ADD cast_id int NOT NULL,
                ALTER TABLE Movie ADD director_id int NOT NULL,
                ALTER TABLE Movie ADD country_id int NOT NULL,
                ALTER TABLE Movie ADD review_id int NOT NULL,

                ALTER TABLE Movie ADD FOREIGN KEY (cast_id) REFERENCES Cast(cast_id),
                ALTER TABLE Movie ADD FOREIGN KEY (director_id) REFERENCES Director(director_id),
                ALTER TABLE Movie ADD FOREIGN KEY (country_id) REFERENCES Country(country_id),
                ALTER TABLE Movie ADD FOREIGN KEY (review_id) REFERENCES Review(review_id)
            """
        )
        self.mysql_cursor.execute(
            """
                ALTER TABLE Review ADDauthor_id int,
                ALTER TABLE Review ADD FOREIGN KEY (author_id) REFERENCES User(user_id)
            """
        )

        print("Successfully Created Tables")

    # This function will return the current connection
    # of the database use this to interact with database query
    # def getCursor(self):
    #     return self.postgres_cursor

    # def getDBConnStatus(self):
    #     # DB STATUS CODE
    #     # Return status: 0 == connected
    #     # Return status: 1 == not connected
    #     return "Connected" if self.postgres_conn.closed == 0 else "Disconnected"