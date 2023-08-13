UPDATE movies
SET
    criterionFormat = "bluray", criterionSpine = _criterion_bluray.'Spine #'
FROM _criterion_bluray
WHERE _criterion_bluray.Title = movies.title
  AND _criterion_bluray.Year = movies.year
  AND owned IS NULL;

UPDATE movies
SET
    criterionFormat = "bluray"
WHERE criterionFormat IS NULL
  AND owned = 'yes'
  AND format = 'bluray'
  AND criterionSpine IS NOT NULL;

UPDATE movies
SET
    criterionFormat = "4K" FROM _criterion_4k
WHERE _criterion_4k.Title = movies.title
  AND _criterion_4k.Year = movies.year;

UPDATE movies
SET
    criterionFormat = "4K", criterionSpine = _criterion_4k.'Spine #'
FROM _criterion_4k
WHERE _criterion_4k.Title = movies.title
  AND _criterion_4k.Year = movies.year;