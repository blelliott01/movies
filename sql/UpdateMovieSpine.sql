SELECT
    *
FROM movies
JOIN _criterion_bluray
WHERE _criterion_bluray.Title = movies.title
  AND _criterion_bluray.Year = movies.year
  AND criterionSpine IS NULL
  --AND criterionFormat IS NULL