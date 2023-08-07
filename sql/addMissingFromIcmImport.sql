BEGIN;

INSERT INTO movies(
	title
	,year
	,owned
	,checked
	,checkedErica
	,url
	,imdburl)
SELECT 
	title
	,year	
	,CASE WHEN owned = 'no' THEN NULL ELSE 'yes' END AS owned
	,CASE WHEN checked = 'no' THEN NULL ELSE 'yes' END AS checked
	,CASE WHEN watchlist = 'no' THEN NULL ELSE 'yes' END AS checkedErica
	,url
	,imdburl
FROM _icm_tsptd_1000 WHERE url NOT IN (SELECT url FROM movies);

COMMIT;