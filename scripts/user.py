from passlib.context import CryptContext
from scripts.database import Database
from scripts.commands import *
from pymongo import ReturnDocument
from datetime import datetime


class User:
    def __init__(self, user_data=""):
        self.pwd_context = CryptContext(
            schemes=["pbkdf2_sha256"],
            default="pbkdf2_sha256",
            pbkdf2_sha256__default_rounds=30000,
        )

        if user_data:
            self.role = "User"
            self.email = user_data["email"]
            self.username = user_data["username"]
            self.description = user_data["description"]
            self.id = user_data["id"]
            self.password = ""
        else:
            self.role = "User"
            self.email = ""
            self.description = ""
            self.username = ""
            self.password = ""
            self.id = ""

        self.activity = []
        self.total_activity = []
        self.review_activity = []
        self.movie_wishlist = []
        self.overview_activity = []
        self.movie_list_graph = []
        self.review_list_graph = []
        self.total_activity_count = 0

        # INSERT USER DATA TO DATABASE
        self.db = Database()
        self.cursor = self.db.getDBCursor()
        self.db_conn = self.db.getDBConn()

    def createUser(self, username, email, password):
        self.password = self.pwd_context.encrypt(password)
        self.username = username
        self.email = email
        self.description = "No description"

        if "mongo" not in self.db.getDB():
            self.cursor.execute(
                INSERT_USER,
                (self.username, self.email, self.password, self.role, self.description),
            )
            self.db.cleanConnection()
        else:
            self.db_conn["moviedb"]["users"].insert_one(
                {
                    "_id": {"username": self.username},
                    "email": self.email,
                    "password": self.password,
                    "role": self.role,
                    "description": self.description,
                    "date_created": datetime.now(),
                    "wishlist": [],
                    "reviewlist": []
                }
            )

    # Password = Password that the user entered in plain text
    # Hash = Hashed password that you retrieve from database
    def verify_pass(self, password, hashed):
        return self.pwd_context.verify(password, hashed)

    def fetchUser(self, username, password):
        if "mongo" not in self.db.getDB():
            self.cursor.execute(FETCH_USER, (username,))

            user_data = self.cursor.fetchall()

            for i in user_data:
                tempId = i[0]
                tempMovieId = i[1]
                tempUsername = i[2]
                tempEmail = i[3]
                tempPass = i[4]
                tempRole = i[5]
                tempDescription = i[6]

                if tempUsername == username and self.verify_pass(password, tempPass):
                    self.username = tempUsername
                    self.password = tempPass
                    self.role = tempRole
                    self.email = tempEmail
                    self.id = tempId
                    self.description = tempDescription
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
            temp_description = ""


            try:
                for key, value in data.items():
                    if "_id" in key:
                        temp_username = value["username"]
                    elif "password" in key:
                        temp_pass = value
                    elif "email" in key:
                        temp_email = value
                    elif "description" in key:
                        temp_description = value

                if temp_username == username and self.verify_pass(password, temp_pass):
                    self.username = temp_username
                    self.password = temp_pass
                    self.email = temp_email
                    self.description = temp_description
                    self.role = "User"
                    print("User successfully logged in")
                    return True
                else:
                    return False
            except AttributeError:
                return False

    def fetchDescription(self):
        if "mongo" not in self.db.getDB():
            # SQL QUERY
            self.cursor.execute(FETCH_USER_DESCRIPTION, (self.id,))
            description = self.cursor.fetchall()

            for i in description:
                self.description = i[0]
        else:
            # MONGO QUERY
            data = self.db_conn["moviedb"]["users"].find_one(
                {"_id": {"username": self.username}}
            )
            
            for key, value in data.items():
                if "description" in key:
                    self.description = value

    def fetchReviewActivity(self):
        if "mongo" not in self.db.getDB():
            # SQL QUERIES
            self.cursor.execute(FETCH_USER_REVIEW_ACTIVITY)
            self.activity = self.cursor.fetchall()

            self.cursor.execute(FETCH_TOTAL_ACTIVITY)
            self.total_activity = self.cursor.fetchall()

            self.cursor.execute(FETCH_REVIEW_ACTIVITY, (self.id,))
            self.review_activity = self.cursor.fetchall()

            self.total_activity_count = sum([i[1] for i in self.total_activity])
        else:
            # MONGO QUERIES
            self.getTotalActivityCount()
            self.getAllReview()
            self.getUserDateActivity()

    def getUserDateActivity(self):
        # Returns all activities by date to be rendered in calendar for profile (Only for mongo)
        if "mongo" in self.db.getDB():
            temp_activities = []
            pipeline = [
                { "$match": { "_id": { "username": self.username }}},
                {
                    "$project": {
                        "all_activities": {
                            "$concatArrays": ["$wishlist", "$reviewlist"]
                        }
                    }
                },
                {
                    "$unwind": "$all_activities"
                },
                {
                    "$group": {
                        "_id": {
                            "$dateToString": {
                                "format": "%Y-%m-%d",
                                "date": "$all_activities.date_created"
                            }
                        },
                        "count": {
                            "$sum": 1
                        }
                    }
                }
            ]

            data = self.db_conn["moviedb"]["users"].aggregate(pipeline)

            for values in data:
                temp_activities.append(values)
            self.total_activity = temp_activities


    def getTotalActivityCount(self):
        # RETURNS TOTAL ACTIVITY COUNT IN MONGO
        pipeline = [
            { "$match": { "_id": {"username": self.username } } },
            {
                "$project": {
                    "total_activity": {
                        "$size": {
                            "$concatArrays": ["$reviewlist", "$wishlist"]
                        }
                    }
                }
            }
        ]

        data = self.db_conn["moviedb"]["users"].aggregate(pipeline)

        for values in data:
            self.total_activity_count = values["total_activity"]

    def getActivity(self):
        # RETURNS ALL USER'S ACTIVITY
        return {
            "activity": self.activity,
            "total_activity": self.total_activity,
            "review_activity": self.review_activity,
            "total_activity_count": self.total_activity_count
        }

    def getAllReview(self):
        # RETURNS ALL REVIEWS FROM A USER IN MONGODB
        data = self.db_conn["moviedb"]["users"].find({ "_id": {"username": self.username }}, {"reviewlist": 1})

        for values in data:
            self.review_activity = values["reviewlist"]

    def fetchMovieWishListActivity(self):
        # RETURNS ALL MOVIES IN USER'S WISHLIST FROM DATABASE
        if "mongo" not in self.db.getDB():
            # SQL QUERIES
            self.cursor.execute(FETCH_MOVIE_WISHLIST_ACTIVITY, (self.id,))
            self.movie_wishlist = self.cursor.fetchall()
        else:
            data = self.db_conn["moviedb"]["users"].find({ "_id": {"username": self.username }}, {"wishlist": 1})

            for values in data:
                self.movie_wishlist = values["wishlist"]

    def fetchOverviewActivity(self):
        if "mongo" not in self.db.getDB():
            # SQL QUERIES
            results = self.cursor.execute(FETCH_OVERVIEW_ACTIVITY, (self.id,), multi=True)

            for i in results:
                if i.with_rows:
                    self.overview_activity = i.fetchall()
        else:
            # MONGO QUERIES
            pipeline = [
                { "$match": { "_id": {"username": self.username } } },
                {
                    "$project": {
                        "overview_activity": {
                            "$concatArrays": ["$reviewlist", "$wishlist"]
                        }
                    }
                }
            ]

            data = self.db_conn["moviedb"]["users"].aggregate(pipeline)

            for values in data:
                self.overview_activity = values["overview_activity"]

    def fetchMovieListGraphActivity(self):
        # RETURNS ALL NECESSARY DATA TO PLOT GRAPH FOR USER'S ACTIVITY WHEN ADDING MOVIES TO WISHLIST
        if "mongo" not in self.db.getDB():
            # SQL QUERIES
            self.cursor.execute(FETCH_MOVIELIST_GRAPH_ACTIVITY, (self.id,))
            self.movie_list_graph = self.cursor.fetchall()
        else:
            # facet allows multiple queries to be done in 1 query
            # MONGO QUERIES
            pipeline = [
                { "$match": { "_id": {"username": self.username} } },
                {
                    "$facet": {
                        "wishlist_graph": [
                            {
                                "$unwind": "$wishlist"
                            },
                            {
                                "$group": {
                                    "_id": {
                                        "$month": "$wishlist.date_created"
                                    },
                                    "count": {
                                        "$sum": 1
                                    }
                                }
                            },
                            {
                                "$sort": {
                                    "_id": 1
                                }
                            }
                        ],
                        "reviewlist_graph": [
                            {"$unwind": "$reviewlist"},
                            {
                                "$group": {
                                    "_id": {
                                        "$month": "$reviewlist.date_created"
                                    },
                                    "count": {
                                        "$sum": 1
                                    }
                                }
                            },
                            {
                                "$sort": {
                                    "_id": 1
                                }
                            }
                        ]
                    }
                }
            ]

            data = self.db_conn["moviedb"]["users"].aggregate(pipeline)
            
            for values in data:
                self.movie_list_graph = values["wishlist_graph"]
                self.review_list_graph = values["reviewlist_graph"]

    def fetchReviewListGraphActivity(self):
        if "mongo" not in self.db.getDB():
            # SQL QUERIES
            self.cursor.execute(FETCH_REVIEWLIST_GRAPH_ACTIVITY, (self.id,))
            self.review_list_graph = self.cursor.fetchall()
        else:
            # MONGO QUERIES
            # QUERY ALREADY IMPLEMENTED IN fetchMovieListGraphActivity()
            pass

    def getUserData(self):
        user_data = {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "role": self.role,
            "description": self.description,
        }

        return user_data

    def addToWishlist(self, movieId, user):
        if "mongo" in self.db.getDB():
            self.db_conn["moviedb"]["users"].find_one_and_update(
                {"_id": {"username": user}},
                {
                    "$push": {
                        "wishlist": {
                            "title": movieId["title"],
                            "release": movieId["release"],
                            "date_created": datetime.now()
                        }
                    },
                },
                return_document=ReturnDocument.AFTER,
            )

            print("Successfully added {0} to wishlist".format(movieId["title"]))
        else:
            movie_id = movieId["id"]
            user_id = user

            self.cursor.execute(
                INSERT_MOVIE_WISHLIST,
                (
                    user_id,
                    movie_id,
                ),
            )

            self.db.cleanConnection()
            print("Successfully added movie to wishlist")

    def getWishList(self, username):
        movie_list = []

        if "mongo" in self.db.getDB():
            # INITIAL PIPELINE THAT CHECKS AGAINST MOVIE WISHLIST WITHOUT THE DATE CREATION IN WISHLIST
            # pipeline = [
            #     {
            #         "$lookup": {
            #             "from": "movies",
            #             "localField": "wishlist",
            #             "foreignField": "_id",
            #             "as": "movie_wishlist",
            #         }
            #     },
            #     {"$match": {"_id.username": username}},
            #     {"$unwind": "$movie_wishlist"},
            #     {
            #         "$project": {
            #             "title": "$movie_wishlist.title",
            #             "poster": "$movie_wishlist.poster",
            #         }
            #     },
            # ]

            pipeline = [
                {
                    "$lookup": {
                        "from": "movies",
                        "localField": "wishlist.title",
                        "foreignField": "title",
                        "as": "movie_wishlist"
                    }
                },
                {"$match": {"_id.username": username }},
                {
                    "$lookup": {
                        "from": "movies",
                        "localField": "wishlist.release",
                        "foreignField": "release",
                        "as": "movie_wishlist"
                    }
                },
                {"$unwind": "$movie_wishlist"},
                {
                    "$project": {
                        "title": "$movie_wishlist.title",
                        "poster": "$movie_wishlist.poster"
                    }
                }
            ]

            data = self.db_conn["moviedb"]["users"].aggregate(pipeline)

            for i in data:
                print(i)
                filtered_name = i["title"].lower().replace(" ", "-")
                movie_list.append({"title": filtered_name, "poster": i["poster"]})
            return movie_list
        else:
            self.cursor.execute(FETCH_MOVIE_WISHLIST, (username,))
            data = self.cursor.fetchall()

            for i in data:
                filtered_name = i[1].lower().replace(" ", "-")
                movie_list.append({"title": filtered_name, "poster": i[0]})

            return movie_list
