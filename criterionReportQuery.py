def getQuery():
    return """
    SELECT 
        title || ' (' || year || ')' AS title
        , criterion || '-' || shelf AS location
    FROM movies
    WHERE criterion IS NOT NULL AND owned = 'yes'
    ORDER BY 
        CASE
            WHEN title LIKE 'A %' THEN SUBSTR(title, 3)
            WHEN title LIKE 'The %' THEN SUBSTR(title, 5)
            ELSE title
        END;
    """