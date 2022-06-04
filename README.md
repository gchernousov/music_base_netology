## Музыкальная база данных

![](/pics/music_base_net.jpg)
  
### 1. __CREATE__ запросы для создания таблиц остались без изменений и находятся в файле *create_md_tables.sql*
  
### 2. __INSERT__ запросы на добавление записей так же не менялись и находятся в файле *insert_md_data.sql*
  
### 3. __SELECT__ запросы для выборки данных:

В некоторых запросах было много результатов, поэтому я выводил только первые 10.

> Количество исполнителей в каждом жанре.

~~~
SELECT genre_name, COUNT(genre_id)
FROM artist_genre ag 
JOIN genres g ON ag.genre_id = g.id
GROUP BY genre_name
ORDER BY COUNT DESC
LIMIT (10);
~~~

Я также добавил сортировку по количеству исполнителей в каждом жанре.

![](/pics/select_result_1.jpg)

> Количество треков, вошедших в альбомы 2019-2020 годов.

~~~
SELECT year, COUNT(*) AS tracks
FROM tracks t
JOIN albums a ON t.album_id = a.id
WHERE year BETWEEN 2019 AND 2020
GROUP BY year;
~~~

![](/pics/select_result_2.jpg)

> Средняя продолжительность треков по каждому альбому.

~~~
SELECT album_name, ROUND((AVG(duration)), 2) AS average
FROM tracks t
JOIN albums a ON t.album_id = a.id 
GROUP BY album_name
LIMIT (10);
~~~

![](/pics/select_result_3.jpg)

> Все исполнители, которые не выпустили альбомы в 2020 году.

~~~
SELECT DISTINCT artist_name
FROM albums ab
JOIN artist_album aa ON ab.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id  
WHERE year != 2020
LIMIT (10);
~~~

![](/pics/select_result_4.jpg)

> Названия сборников, в которых присутствует конкретный исполнитель.

Например, сборники, где есть композиции группы *Mogwai*.

~~~
SELECT compilation_name 
FROM compilations c
JOIN compilation_track ct ON c.id = ct.compilation_id 
JOIN tracks t ON ct.track_id = t.id 
JOIN albums ab ON t.album_id = ab.id 
JOIN artist_album aa ON ab.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id 
WHERE ar.artist_name = 'Mogwai';
~~~

![](/pics/select_result_5.jpg)

> Название альбомов, в которых присутствуют исполнители более 1 жанра.

~~~
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
~~~

![](/pics/select_result_6.jpg)

> Наименование треков, которые не входят в сборники.

~~~
SELECT track_name 
FROM tracks t
LEFT JOIN compilation_track ct ON t.id = ct.track_id
WHERE ct.track_id IS NULL
LIMIT (10);
~~~

![](/pics/select_result_7.jpg)

> Исполнители, написавшие самый короткий по продолжительности трек.

~~~
SELECT artist_name
FROM artists ar
JOIN artist_album aa ON ar.id = aa.artist_id 
JOIN albums ab ON aa.album_id = ab.id
JOIN tracks t ON ab.id = t.album_id
WHERE duration = (SELECT MIN(duration) FROM tracks t);
~~~

![](/pics/select_result_8.jpg)

> Название альбомов, содержащих наименьшее количество треков.

Этот запрос действительно вызвал сложности, в отличие от остальных.
Не уверен в правильности его реализации, но результат выводится верный.

~~~
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
~~~

В моей базе действительно есть один альбом, состоящий всего из 3х треков.

![](/pics/select_result_9.jpg)

Все запросы в файле *select_md.sql*