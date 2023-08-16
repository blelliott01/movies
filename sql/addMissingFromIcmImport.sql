BEGIN;

INSERT INTO movies(
	title
	,year
	,owned
	,checkedLee
	,checkedErica
	,url
	,imdburl)
SELECT 
	title
	,year	
	,CASE WHEN owned = 'no' THEN NULL ELSE 'yes' END AS owned
	,CASE WHEN checked = 'no' THEN NULL ELSE 'yes' END AS checkedLee
	,CASE WHEN watchlist = 'no' THEN NULL ELSE 'yes' END AS checkedErica
	,url
	,imdburl
FROM _icm_criterion_bluray WHERE url NOT IN (SELECT url FROM movies);

COMMIT;