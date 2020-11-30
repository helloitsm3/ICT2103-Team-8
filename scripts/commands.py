# SECTION FOR ALL INSERT COMMANDS

INSERT_MOVIE = """
    INSERT INTO Movie (
        ratings, 
        run_time,
        poster_path, 
        plot, 
        title,
        release_date
    ) VALUES (%s, %s, %s, %s, %s, %s)
"""

INSERT_REVIEW = """
    INSERT INTO review (
        author_id, movie_id, points, review
    ) VALUES (%s, %s, %s, %s)
"""

INSERT_USER = """
    INSERT INTO User (username, email, password, role_id, description) VALUES (%s, %s, %s, %s, %s)
"""

INSERT_MOVIE_WISHLIST = """
    INSERT INTO movielist (user_id, movie_id) VALUES (%s, %s)
"""

# SECTION FOR ALL FETCH COMMANDS
# FETCH USER SECTION

FETCH_USER = """
    SELECT * FROM User WHERE username = %s
"""

FETCH_USER_DESCRIPTION = """
    SELECT description FROM User WHERE user_id = %s
"""

# FETCH MOVIE SECTION

FETCH_MOVIE_WISHLIST = """
    SELECT 
	    m.poster_path,
        m.title
    FROM Movielist ml
    INNER JOIN Movie m ON ml.movie_id = m.movie_id
    INNER JOIN User u ON ml.user_id = u.user_id
    WHERE
	    ml.user_id = %s;
"""

FETCH_TOP_TEN_MOVIE_NAME = """
    SELECT title FROM movie ORDER BY ratings DESC LIMIT 10
"""

FETCH_MOVIE = """ 
    SELECT * FROM Movie WHERE poster_path=%s
"""

FETCH_ALL_REVIEW = """
    SELECT 
        u.username, r.review, r.points 
    FROM 
        Review r 
    INNER JOIN User u 
    ON r.author_id = u.user_id AND r.movie_id = %s
"""

FETCH_MOVIE_BY_NAME = """
    SELECT * FROM Movie WHERE LOWER(title)=%s
"""

FETCH_RATINGS = """
    SELECT AVG(r.points) AS ratings 
    FROM 
        Review r 
    INNER JOIN User u ON r.author_id = u.user_id AND r.movie_id = %s;
"""

FETCH_FROM_MOVIE_SEARCH = """
    SELECT M.poster_path, M.title, D.director_name, M.run_time, M.ratings
    FROM
        movie M
    LEFT JOIN director D ON M.director_id = D.director_id
    WHERE
        title LIKE %s ORDER BY ratings DESC
"""

# FETCH PROFILE ACTIVITY SECTION

FETCH_USER_REVIEW_ACTIVITY = """
    SELECT 
        COUNT(review),
        DATE(date_create)
    FROM Review
    GROUP BY DATE(Review.date_create)
"""

FETCH_TOTAL_ACTIVITY = """
    SELECT Date, Count(Date)
    FROM (
            SELECT DATE(date_created) AS Date
            FROM movie_list ml
            WHERE user_id = %s
            
            UNION ALL
            
            SELECT DATE(date_create) AS Date
            FROM review_list rl
            WHERE user_id = %s
    ) AS temp
    GROUP BY Date
"""

FETCH_REVIEW_ACTIVITY = """
    SELECT 
        r.review,
        r.date_create,
        m.title
    FROM 
        Review r 
    INNER JOIN User u ON r.author_id = u.user_id
    INNER JOIN Movie m ON r.movie_id = m.movie_id
    WHERE
        user_id = %s
    ORDER BY
        DATE(r.date_create) DESC
"""

FETCH_MOVIE_WISHLIST_ACTIVITY = """
    SELECT 
        ml.date_created,
        m.title
    FROM 
        Movielist ml 
    INNER JOIN User u ON ml.user_id = u.user_id
    INNER JOIN Movie m ON ml.movie_id = m.movie_id
    WHERE
        ml.user_id = %s
    ORDER BY
        DATE(ml.date_created) DESC
"""

FETCH_OVERVIEW_ACTIVITY = """
    CREATE OR REPLACE VIEW review_list AS
    SELECT 
        r.review,
        r.date_create,
        m.title,
        m.movie_id,
        u.user_id
    FROM 
        Review r 
    INNER JOIN User u ON r.author_id = u.user_id
    INNER JOIN Movie m ON r.movie_id = m.movie_id
    ORDER BY
        DATE(r.date_create) DESC;


    CREATE OR REPLACE VIEW movie_list AS
    SELECT 
        ml.date_created,
        m.title,
        m.movie_id,
        ml.user_id
    FROM 
        Movielist ml 
    INNER JOIN User u ON ml.user_id = u.user_id
    INNER JOIN Movie m ON ml.movie_id = m.movie_id
    ORDER BY
        DATE(ml.date_created) DESC;


    SELECT * 
    FROM (
        SELECT title, date_created, movie_id, user_id, NULL AS review 
        FROM movie_list ml
        UNION ALL
        SELECT title, date_create, movie_id, user_id, review
        FROM review_list rl
    ) temp
    WHERE 
        temp.user_id = %s
"""

FETCH_MOVIELIST_GRAPH_ACTIVITY = """
    SELECT DATE_FORMAT(date_created, '%m') AS Date_Created, COUNT(DATE_FORMAT(date_created, '%m')) AS activity_count
    FROM movie_list
    WHERE user_id = %s
    GROUP BY DATE_FORMAT(date_created, '%m')
"""

FETCH_REVIEWLIST_GRAPH_ACTIVITY = """
    SELECT DATE_FORMAT(date_create, '%m') AS Date_Created, COUNT(DATE_FORMAT(date_create, '%m')) AS activity_count
    FROM review_list rl
    WHERE user_id = %s
    GROUP BY DATE_FORMAT(date_create, '%m')
"""

# SECTION FOR ALL ALTER COMMANDS
ALTER_USER_DESCRIPTION = """
    UPDATE user
    SET 
        description = %s
    WHERE
        user_id = %s
"""


# SECTION FOR ALL CREATE TABLE COMMANDS
CREATE_USER_TBL = """
    CREATE TABLE IF NOT EXISTS User (
        user_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
        movie_id INT, 
        username VARCHAR(50) NOT NULL UNIQUE, 
        email VARCHAR(50) NOT NULL, 
        password VARCHAR(255) NOT NULL, 
        role VARCHAR(25), 
        description VARCHAR(255),
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
    )
"""

CREATE_DIRECTOR_TBL = """
    CREATE TABLE IF NOT EXISTS Director (
        director_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
        director_name VARCHAR(100) NOT NULL UNIQUE
    )
"""

CREATE_MOVIE_TBL = """
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
    )
"""

CREATE_REVIEW_TBL = """
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
)
"""


CREATE_MOVIE_LIST_TBL = """
CREATE TABLE IF NOT EXISTS MovieList (
    user_id INT,
    movie_id INT,
    date_created DATETIME DEFAULT CURRENT_TIMESTAMP,

    FOREIGN KEY (user_id) REFERENCES User(user_id) ON DELETE CASCADE,
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id) ON DELETE CASCADE,
    CONSTRAINT uc_movielist UNIQUE (user_id, movie_id) 
)
"""


CREATE_TIMESLOT_TBL = """
CREATE TABLE IF NOT EXISTS Timeslot (
    showtime_id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    slots VARCHAR(100),
    date_showing DATETIME DEFAULT CURRENT_TIMESTAMP
)
"""


CREATE_SHOWTIME_TBL = """
CREATE TABLE IF NOT EXISTS Showtime (
    movie_id INT,
    showtime_id INT,

    FOREIGN KEY (showtime_id) REFERENCES Timeslot(showtime_id),
    FOREIGN KEY (movie_id) REFERENCES Movie(movie_id)
)
"""