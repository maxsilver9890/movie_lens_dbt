WITH raw_links AS (
    SELECT * FROM MOVIELENS.RAW.RAW_LINKS
)
SELECT 
    movieId AS movie_id,
    imdbld AS imdb_id,
    tmdbld AS tmdb_id
FROM raw_links