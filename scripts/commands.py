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


# SECTION FOR ALL FETCH COMMANDS
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

# SECTION FOR ALL CREATE TABLE COMMANDS
CREATE_USER_TBL = """
    CREATE TABLE IF NOT EXISTS User (
        user_id INT PRIMARY KEY AUTO_INCREMENT NOT NULL, 
        movie_id INT, 
        username VARCHAR(50) NOT NULL UNIQUE, 
        email VARCHAR(50) NOT NULL, 
        password VARCHAR(255) NOT NULL, 
        role_id VARCHAR(25), 
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP 
    )
"""