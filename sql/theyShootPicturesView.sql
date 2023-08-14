DROP VIEW IF EXISTS they_shoot_pictures_view;

CREATE VIEW they_shoot_pictures_view AS
SELECT
    tspdt
    ,title
	,director
	,year
	,runtime
	,owned
	,ownedFormat
	,criterionSpine
	,shelf
	,checkedLee
FROM Movies 
WHERE tspdt IS NOT NULL
ORDER BY tspdt;
