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
            self.mysql_conn.autocommit = True
            self.mysql_cursor = self.mysql_conn.cursor()
            # self.postgres_cursor = self.postgres_conn.cursor()
        except:
            print("Fail to connect to the database")

    def getMySQLCursor(self):
        return self.mysql_cursor

    def getMySQLConn(self):
        return self.mysql_conn

    # Function to create all necessary tables
    def initMySQLTable(self):
        # MYSQL ROLE TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Role (
                    role_id INT PRIMARY KEY AUTO_INCREMENT,
                    role_tag VARCHAR(25) UNIQUE,
                    role_name VARCHAR(25) UNIQUE
                )"""
        )

        # MYSQL USER TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS User (
                    user_id INT PRIMARY KEY AUTO_INCREMENT,
                    username VARCHAR(100) NOT NULL UNIQUE,
                    email VARCHAR(100) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    role_id INT,
                    movie_id INT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (role_id) REFERENCES Role(role_id)
                )"""
        )

        # MYSQL GENRE TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Genre (
                    genre_id INT PRIMARY KEY AUTO_INCREMENT,
                    name VARCHAR(255) NOT NULL
                )"""
        )

        # MYSQL COUNTRY TABLE
        self.mysql_cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS Country (
                    country_id INT PRIMARY KEY AUTO_INCREMENT,
                    country_name VARCHAR(100) NOT NULL
            )"""
        )

        # MYSQL REVIEW TABLE
        self.mysql_cursor.execute(
            """
                CREATE TABLE IF NOT EXISTS Review (    
                    review_id INT PRIMARY KEY AUTO_INCREMENT,             
                    points INT NOT NULL,
                    author INT NOT NULL,
                    review VARCHAR(2500) NOT NULL,
                    date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    
                    FOREIGN KEY (author) REFERENCES User(user_id)
            )"""
        )

        # MYSQL MOVIE TABLE
        self.mysql_cursor.execute(
            """ 
                CREATE TABLE IF NOT EXISTS Movie (
                    movie_id INT PRIMARY KEY AUTO_INCREMENT,
                    ratings INT,
                    run_time INT,
                    country_id INT,
                    writer_id INT,
                    director_id INT,
                    review_id INT,
                    genre_id INT,
                    cast_id INT,

                    poster_path VARCHAR(255) NOT NULL,
                    plot VARCHAR(2500) NOT NULL,
                    title VARCHAR(100) NOT NULL,
                    overview VARCHAR(255) NOT NULL,
                    original_language VARCHAR(15) NOT NULL,
                    release_date DATETIME DEFAULT CURRENT_TIMESTAMP,

                    FOREIGN KEY (country_id) REFERENCES Country(country_id),
                    FOREIGN KEY (writer_id) REFERENCES User(user_id),
                    FOREIGN KEY (director_id) REFERENCES User(user_id),
                    FOREIGN KEY (cast_id) REFERENCES User(user_id),
                    FOREIGN KEY (review_id) REFERENCES Review(review_id),
                    FOREIGN KEY (genre_id) REFERENCES Genre(genre_id)
            )"""
        )

        # ALTER USER TABLE COMMAND
        self.mysql_cursor.execute(
            """
            ALTER TABLE User ADD FOREIGN KEY (movie_id) REFERENCES Movie(movie_id);
            """
        )

        self.mysql_cursor.execute(
            "INSERT INTO Role (role_tag, role_name) VALUES ('admin', 'Administrator');"
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