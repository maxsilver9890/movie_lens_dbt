

def top_rated_movies_summary():
    return """
    WITH ratings_summary AS (
      SELECT
        movie_id,
        AVG(rating) AS average_rating,
        COUNT(*) AS total_ratings
      FROM MOVIELENS.DEV.fct_ratings
      GROUP BY movie_id
      HAVING COUNT(*) > 100
    )

    SELECT
      m.movie_title,
      rs.average_rating,
      rs.total_ratings
    FROM ratings_summary rs
    JOIN MOVIELENS.DEV.dim_movies m ON m.movie_id = rs.movie_id
    ORDER BY rs.average_rating DESC;
    """

def user_engagement():
    return """
    SELECT
      user_id,
      COUNT(*) AS number_of_ratings,
      AVG(rating) AS average_rating_given
    FROM MOVIELENS.DEV.fct_ratings
    GROUP BY user_id
    ORDER BY number_of_ratings DESC;
    """

def rating_over_the_years():
    return """
    SELECT
  EXTRACT(YEAR FROM rating_timestamp) AS rating_year,
  COUNT(*) AS ratings_given
FROM MOVIELENS.DEV.fct_ratings
WHERE rating_timestamp IS NOT NULL
GROUP BY rating_year
ORDER BY rating_year;


    """

def tag_relevance_analysis():
    return """
    SELECT
      t.tag_name,
      AVG(gs.relevance_score) AS avg_relevance,
      COUNT(DISTINCT gs.movie_id) AS movies_tagged
    FROM MOVIELENS.DEV.fct_genome_scores gs
    JOIN MOVIELENS.DEV.dim_genome_tags t ON gs.tag_id = t.tag_id
    GROUP BY t.tag_name
    ORDER BY avg_relevance DESC;
    """

# This query is having some issues

# def genre_rating_distribution():
#     return """
#     SELECT
#       genre.value::STRING AS genre,
#       AVG(r.rating) AS average_rating,
#       COUNT(DISTINCT m.movie_id) AS total_movies
#     FROM MOVIELENS.DEV.dim_movies_with_tags m,
#          LATERAL FLATTEN(input => SPLIT(m.genres, '|')) genre
#     JOIN MOVIELENS.DEV.fct_ratings r ON m.movie_id = r.movie_id
#     WHERE r.rating IS NOT NULL
#     GROUP BY genre.value
#     ORDER BY average_rating DESC
#     LIMIT 100;
#     """

def genre_analysis():
    """
    NEW QUERY: Analyzes genres by counting movies and calculating average ratings.
    """
    return """
    WITH movie_genres AS (
      SELECT
        m.movie_id,
        g.value::STRING AS genre
      FROM MOVIELENS.DEV.dim_movies m,
           LATERAL FLATTEN(input => SPLIT(m.genres, '|')) g
    )
    SELECT
      mg.genre,
      COUNT(DISTINCT mg.movie_id) as number_of_movies,
      AVG(r.rating) as average_rating
    FROM movie_genres mg
    JOIN MOVIELENS.DEV.fct_ratings r ON mg.movie_id = r.movie_id
    WHERE mg.genre != '(no genres listed)'
    GROUP BY mg.genre
    ORDER BY number_of_movies DESC;
    """