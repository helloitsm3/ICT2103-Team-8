from passlib.context import CryptContext
from scripts.database import Database


class User:
    def __init__(self, username, email, password):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000,
        )

        self.role = "User"
        self.email = email
        self.username = username
        self.password = self.pwd_context.encrypt(password)

        # # INSERT USER DATA TO DATABASE
        # db = Database(database="mysql")
        # cursor = db.getDBCursor()
        # cursor.execute(
        #     "INSERT INTO User (username, email, password, role_id) VALUES ({0}, {1}, {2}, {3})".format(
        #         username, email, self.password, role
        #     )
        # )

    # Password = Password that the user entered in plain text
    # Hash = Hashed password that you retrieve from database
    def verify_pass(self, password, hashed):
        return self.pwd_context.verify(password, hashed)