DROP VIEW shelf_view;

CREATE VIEW shelf_view AS
SELECT
    title
	,director
	,year
	,runtime
	,tspdt
	,criterionSpine
	,shelf
	,checkedLee
FROM Movies 
WHERE shelf IS NOT NULL
ORDER BY 
  CASE 
    WHEN title LIKE 'A %' THEN SUBSTR(title, 3)
    WHEN title LIKE 'The %' THEN SUBSTR(title, 5)
    ELSE title
  END