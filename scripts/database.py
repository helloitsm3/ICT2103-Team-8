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

    # This function will return the current connection
    # of the database use this to interact with database query
    # def getCursor(self):
    #     return self.postgres_cursor

    # def getDBConnStatus(self):
    #     # DB STATUS CODE
    #     # Return status: 0 == connected
    #     # Return status: 1 == not connected
    #     return "Connected" if self.postgres_conn.closed == 0 else "Disconnected"