import os
from dotenv import load_dotenv

load_dotenv()


DB_CONFIG_READ = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD"),
    "database": os.getenv("DB_NAME"),
}

DB_CONFIG_WRITE = {
    "host": os.getenv("DB_HOST_WRITE"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER_WRITE"),
    "password": os.getenv("DB_PASSWORD_WRITE"),
}


main_table = """
WITH main_table AS
(
SELECT 
    f.title,
    f.release_year,
    c.name AS genre,
    GROUP_CONCAT(CONCAT(a.first_name, ' ', a.last_name) SEPARATOR ', ') AS actors
FROM film f
JOIN film_actor fa USING(film_id)
JOIN actor a USING(actor_id)
LEFT JOIN film_category fc USING(film_id)
LEFT JOIN category c USING(category_id)
GROUP BY f.title, f.release_year, c.name
)
"""

table_for_actors = """
WITH actors_table AS 
(
SELECT 
    f.title,
    f.release_year,
	 c.name as genre,
    CONCAT(a.first_name, ' ', a.last_name) AS Actor
FROM film f
JOIN film_actor fa USING(film_id)
JOIN actor a USING(actor_id)
LEFT JOIN film_category fc USING(film_id)
LEFT JOIN category c USING(category_id)
)
"""