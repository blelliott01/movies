SELECT
    *
FROM movies
WHERE url IN (
SELECT
    url
FROM _icm_criterion_blueray)
and url IN (
SELECT
    url
FROM _icm_tspdt_1000)
and owned is null
order by rankTheyShoot