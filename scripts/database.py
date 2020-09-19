import psycopg2
import os

DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")


class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                """
                dbname={0}
                host={1}
                user={2}
                password={3}
                sslmode=require
                """.format(
                    DB_NAME, DB_HOST, DB_USER, DB_PASS
                )
            )
        except:
            print("Fail to connect to the database")

        self.cursor = self.conn.cursor()

    def getCursor(self):
        return self.cursor

    def getDBConnStatus(self):
        # DB STATUS CODE
        # Return status: 0 == connected
        # Return status: 1 == not connected
        return "Connected" if self.conn.closed == 0 else "Disconnected"