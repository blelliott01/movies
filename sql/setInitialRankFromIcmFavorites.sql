UPDATE movies SET rank = NULL;

UPDATE movies
SET rank = (
    SELECT row_num
    FROM (
        SELECT m.imdburl, 
               ROW_NUMBER() OVER (ORDER BY f.officialtoplistcount DESC) AS row_num
        FROM movies AS m
        INNER JOIN _icm_favorited AS f ON m.imdburl = f.imdburl
    ) AS ranked
    WHERE ranked.imdburl = movies.imdburl
);