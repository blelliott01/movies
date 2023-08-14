DROP VIEW IF EXISTS owned_or_available_view;

CREATE VIEW owned_or_available_view AS
SELECT
    title
	,director
	,year
	,runtime
	,metacriticRating
	,imdbRating
	,criterionSpine
	,criterionFormat
	,shelf
	,tspdt
	,top100
	,checkedLee
FROM Movies 
WHERE (owned = 'yes' AND shelf IS NOT NULL)
OR (tspdt IS NOT NULL AND criterionFormat IS NOT NULL)
ORDER BY 
  CASE 
    WHEN title LIKE 'A %' THEN SUBSTR(title, 3)
    WHEN title LIKE 'The %' THEN SUBSTR(title, 5)
    ELSE title
  END;