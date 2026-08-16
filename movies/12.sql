-- 12. Titles of all of movies in which both Jennifer Lawrence and Bradley Cooper starred
SELECT title FROM movies WHERE id IN(
    SELECT movie_id FROM stars
    WHERE person_id IN (
        SELECT id FROM people WHERE name IN ('Bradley Cooper', 'Jennifer Lawrence')
    )
    GROUP BY movie_id
    HAVING COUNT(DISTINCT person_id) = 2
);
