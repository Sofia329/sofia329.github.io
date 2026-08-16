-- 11. Titles of the five highest rated movies (in order) that Chadwick Boseman starred in, starting with the highest rated
-- picked out all movie id charwick has casted

SELECT m.title
FROM movies m, ratings r, stars s, people p
WHERE m.id = r.movie_id
AND r.movie_id = s.movie_id
AND s.person_id = p.id
AND p.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5;
