UPDATE movies
SET
    tspdt2k = _icm_tspdt_20th.rank
FROM _icm_tspdt_20th
WHERE movies.url = _icm_tspdt_20th.url  
