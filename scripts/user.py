from passlib.context import CryptContext
from scripts.database import Database


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

        # # INSERT USER DATA TO DATABASE
        self.db = Database(database="mysql")
        self.cursor = self.db.getDBCursor()

    def createUser(self, username, email, password):
        self.password = self.pwd_context.encrypt(password)
        self.username = username
        self.email = email

        self.cursor.execute(
            "INSERT INTO User (username, email, password, role_id) VALUES (%s, %s, %s, %s)",
            (self.username, self.email, self.password, self.role),
        )
        self.db.cleanConnection()

    # Password = Password that the user entered in plain text
    # Hash = Hashed password that you retrieve from database
    def verify_pass(self, password, hashed):
        return self.pwd_context.verify(password, hashed)

    def fetchUser(self, username, password):
        self.cursor.execute(
            "SELECT username, password FROM User WHERE username = %s", (username,)
        )

        user_data = self.cursor.fetchall()

        for i in user_data:
            tempU = i[0]
            tempP = i[1]

            if tempU == username and self.verify_pass(password, tempP):
                self.username = tempU
                self.password = tempP
                print("User successfully logged in")
                return True
            else:
                print("User login failed")
        self.db.cleanConnection()
