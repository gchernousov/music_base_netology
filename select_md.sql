SELECT genre_name, COUNT(genre_id)
FROM artist_genre ag 
JOIN genres g ON ag.genre_id = g.id
GROUP BY genre_name
ORDER BY COUNT DESC
LIMIT (10);


SELECT year, COUNT(*) AS tracks
FROM tracks t
JOIN albums a ON t.album_id = a.id
WHERE year BETWEEN 2019 AND 2020
GROUP BY year;


SELECT album_name, ROUND((AVG(duration)), 2) AS average
FROM tracks t
JOIN albums a ON t.album_id = a.id 
GROUP BY album_name
LIMIT (10);


SELECT DISTINCT artist_name
FROM albums ab
JOIN artist_album aa ON ab.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id  
WHERE year != 2020
LIMIT (10);


SELECT compilation_name 
FROM compilations c
JOIN compilation_track ct ON c.id = ct.compilation_id 
JOIN tracks t ON ct.track_id = t.id 
JOIN albums ab ON t.album_id = ab.id 
JOIN artist_album aa ON ab.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id 
WHERE ar.artist_name = 'Mogwai';


SELECT album_name
FROM (
	SELECT artist_id, COUNT(artist_id) AS genres
	FROM artist_genre
	GROUP BY artist_id) AS t1
JOIN artists ar ON t1.artist_id = ar.id
JOIN artist_album aa ON ar.id = aa.artist_id 
JOIN albums ab ON aa.album_id = ab.id
WHERE genres > 1
LIMIT (10);


SELECT track_name 
FROM tracks t
LEFT JOIN compilation_track ct ON t.id = ct.track_id
WHERE ct.track_id IS NULL
LIMIT (10);


SELECT artist_name
FROM artists ar
JOIN artist_album aa ON ar.id = aa.artist_id 
JOIN albums ab ON aa.album_id = ab.id
JOIN tracks t ON ab.id = t.album_id
WHERE duration = (SELECT MIN(duration) FROM tracks t);


SELECT album_name, MIN(nt)
FROM albums a
JOIN (
	SELECT album_id, COUNT(album_id) nt
	FROM tracks 
	GROUP BY album_id) AS t1 ON a.id = t1.album_id
GROUP BY album_name
HAVING MIN(nt) = (
	SELECT MIN(COUNT)
	FROM (
		SELECT album_id, COUNT(album_id)
		FROM tracks 
		GROUP BY album_id) AS t1);