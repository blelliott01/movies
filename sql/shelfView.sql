DROP VIEW location_view;

CREATE VIEW location_view AS
SELECT
    title
	,director
	,year
	,runtime
	,tspdt
	,criterionId
	,location
	,checkedLee
FROM Movies 
WHERE location IS NOT NULL
ORDER BY 
  CASE 
    WHEN title LIKE 'A %' THEN SUBSTR(title, 3)
    WHEN title LIKE 'The %' THEN SUBSTR(title, 5)
    ELSE title
  END