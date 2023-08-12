SELECT json_extract(omdbData, '$.Poster') FROM movies WHERE omdbData IS NOT NULL
