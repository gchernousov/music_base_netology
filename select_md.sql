SELECT album_name, year 
FROM albums
WHERE year = 2018;

SELECT track_name, duration
FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);

SELECT track_name, duration
FROM tracks
WHERE duration > (3 * 60) + 30;

SELECT compilation_name, year
FROM compilations
WHERE year BETWEEN 2018 AND 2020;

SELECT artist_name
FROM artists
WHERE artist_name NOT LIKE '% %';

SELECT track_name
FROM tracks
WHERE track_name ILIKE '%my%';