UPDATE movies
SET rating = 
  CASE
    WHEN json_extract(value, '$.Source') = 'Metacritic' THEN CAST(REPLACE(json_extract(value, '$.Value'), '/100', '') AS INTEGER)
    WHEN json_extract(value, '$.Source') = 'Internet Movie Database' THEN CAST(REPLACE(json_extract(value, '$.Value'), '/10', '') AS INTEGER) * 10
  END
FROM json_each(json_extract(movies.omdbData, '$.Ratings'))
WHERE movies.omdbData IS NOT NULL
  AND (json_extract(value, '$.Source') = 'Metacritic' OR json_extract(value, '$.Source') = 'Internet Movie Database');