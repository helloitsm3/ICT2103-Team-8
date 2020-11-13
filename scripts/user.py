from passlib.context import CryptContext
from scripts.database import Database
from scripts.commands import *


class User:
    def __init__(self):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000,
        )

        self.role = "User"
        self.email = ""
        self.username = ""
        self.password = ""
        self.id = ""

        # INSERT USER DATA TO DATABASE
        self.db = Database()
        # self.cursor = self.db.getDBCursor()
        self.db_conn = self.db.getDBConn()

    def createUser(self, username, email, password):
        self.password = self.pwd_context.encrypt(password)
        self.username = username
        self.email = email

        if "mongo" not in self.db.getDB():
            self.cursor.execute(
                INSERT_USER,
                (self.username, self.email, self.password, self.role),
            )
            self.db.cleanConnection()
        else:
            self.db_conn["moviedb"]["users"].insert_one(
                {
                    "_id": {"username": self.username},
                    "email": self.email,
                    "password": self.password,
                    "role": self.role,
                }
            )

    # Password = Password that the user entered in plain text
    # Hash = Hashed password that you retrieve from database
    def verify_pass(self, password, hashed):
        return self.pwd_context.verify(password, hashed)

    def fetchUser(self, username, password):
        if "mongo" not in self.db.getDB():
            self.cursor.execute("SELECT * FROM User WHERE username = %s", (username,))

            user_data = self.cursor.fetchall()

            for i in user_data:
                tempId = i[0]
                tempMovieId = i[1]
                tempUsername = i[2]
                tempEmail = i[3]
                tempPass = i[4]
                tempRole = i[5]

                if tempUsername == username and self.verify_pass(password, tempPass):
                    self.username = tempUsername
                    self.password = tempPass
                    self.role = tempRole
                    self.email = tempEmail
                    self.id = tempId
                    print("User successfully logged in")
                    return True
                else:
                    print("User login failed")
                    return False
            self.db.cleanConnection()
        else:
            # FOR ALL MONGO QUERIES
            data = self.db_conn["moviedb"]["users"].find_one(
                {"_id": {"username": username}}
            )

            temp_username = ""
            temp_pass = ""
            temp_email = ""

            try:
                for key, value in data.items():
                    if "_id" in key:
                        temp_username = value["username"]
                    elif "password" in key:
                        temp_pass = value
                    elif "email" in key:
                        temp_email = value

                if temp_username == username and self.verify_pass(password, temp_pass):
                    self.username = temp_username
                    self.password = temp_pass
                    self.role = "User"
                    self.email = temp_email
                    print("User successfully logged in")
                    return True
                else:
                    return False
            except AttributeError:
                return False

    def getUserData(self):
        user_data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
        }

        return user_data

    def createMovieList(self, movieId):
        pass