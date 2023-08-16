--UPDATE movies set 
--imdbRating = null, 
--metacriticRating = null,
--director = null,
--runtime = null;

--UPDATE movies
--SET metacriticRating = CAST(REPLACE(json_extract(value, '$.Value'), '/100', '') AS INTEGER)
--FROM json_each(json_extract(movies.omdbData, '$.Ratings'))
--WHERE movies.omdbData IS NOT NULL AND json_extract(value, '$.Source') = 'Metacritic';

--UPDATE movies
--SET imdbRating = CAST(CAST(REPLACE(json_extract(value, '$.Value'), '/10', '') AS REAL) * 10 AS INTEGER)
--FROM json_each(json_extract(movies.omdbData, '$.Ratings'))
--WHERE movies.omdbData IS NOT NULL AND json_extract(value, '$.Source') = 'Internet Movie Database';

UPDATE movies 
set director = json_extract(omdbData, '$.Director'),
runtime = CAST(REPLACE(json_extract(omdbData, '$.Runtime'), ' min', '') AS INTEGER)
WHERE director IS NULL;