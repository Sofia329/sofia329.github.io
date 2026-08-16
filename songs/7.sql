SELECT AVG(energy)
FROM songs
WHERE artist_id = (
    SELECT id FROM artists WHERE name = 'Drake'
);

/*
SELECT AVG(energy)
FROM songs
JOIN artists
ON songs.artist_id = artists.id
WHERE artists.name = 'Drake';

*/
