## Музыкальная база данных

### 1. Структура базы данных.

![](/pics/music_base_net.jpg)
  
__CREATE__ запросы для создания таблиц:

~~~
CREATE TABLE genres(
	id SERIAL PRIMARY KEY,
	genre_name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE artists(
	id SERIAL PRIMARY KEY,
	artist_name VARCHAR(100) NOT NULL
);

CREATE TABLE albums (
	id SERIAL PRIMARY KEY,
	album_name VARCHAR(100) NOT NULL,
	year INTEGER NOT NULL,
);

CREATE TABLE tracks(
	id SERIAL PRIMARY KEY,
	track_position INTEGER NOT NULL,
	track_name VARCHAR(100) NOT NULL,
	duration INTEGER NOT NULL,
	album_id INTEGER NOT NULL REFERENCES albums(id)
);

CREATE TABLE artist_genre(
	artist_id INTEGER REFERENCES artists(id),
	genre_id INTEGER REFERENCES genres(id),
	CONSTRAINT art_gen PRIMARY KEY (artist_id, genre_id)
);

CREATE TABLE artist_album(
	artist_id INTEGER REFERENCES artists(id),
	album_id INTEGER REFERENCES albums(id),
	CONSTRAINT art_alb PRIMARY KEY (artist_id, album_id)
);

CREATE TABLE compilations(
	id SERIAL PRIMARY KEY,
	compilation_name VARCHAR(100) NOT NULL,
	year INTEGER NOT NULL,
);

CREATE TABLE compilation_track(
	compilation_id INTEGER REFERENCES compilations(id),
	track_id INTEGER REFERENCES tracks(id),
	CONSTRAINT comp_trck PRIMARY KEY (compilation_id, track_id)
);
~~~

Все запросы находятся в файле *create_md_tables.sql*
  
### 2. __INSERT__ запросы на добавление записей.
  
Добавление информации об альбоме на примере *Korn - 1999 - Issues*:
  
Добавим название исполнителя:

~~~
INSERT INTO artists (artist_name)
VALUES ('Korn');
~~~

С помощью `SELECT * FROM artists WHERE artist_name = 'Korn';` можем узнать __id__ необходимого исполнителя.
Но можно сделать другой запрос, чтоб узнать __id__ только что добавленной записи:

~~~
SELECT * FROM artists
ORDER BY id DESC
LIMIT (1);
~~~

Добавим жанр:

~~~
INSERT INTO genres (genre_name)
VALUES ('Nu Metal');
~~~

__id__ группы *Korn* - 49, __id__ *Nu Metal* - 27. 
Установим связь:

~~~
INSERT INTO artist_genre VALUES (49, 27);
~~~

Теперь добавим альбом:

~~~
INSERT INTO albums (album_name, year)
VALUES ('Issues', 1999);
~~~

И также добавим связь альбома и исполнителя, где __id__ только что добавленного альбома - 25:

~~~
INSERT INTO artist_album VALUES (49, 25);
~~~

Осталось добавить композиции:

~~~
INSERT INTO tracks (track_name, duration, album_id, track_position)
VALUES ('Dead', 72, 25, 1);

INSERT INTO tracks (track_name, duration, album_id, track_position)
VALUES ('Falling Away From Me', 270, 25, 2);
~~~

Можно сразу добавить несколько записей. Например:

~~~
INSERT INTO tracks (track_name, duration, album_id, track_position)
VALUES ('Trash', 206, 25, 3), ('4 U', 102, 25, 4), ('Beg for Me', 233, 25, 5);
~~~

Чтобы удостовериться, что все данные и связи внесены верно, можно сделать такой __SELECT__ запрос:

~~~
SELECT artist_name, year, album_name, track_position, track_name, duration
FROM tracks t
JOIN albums r ON t.album_id = r.id
JOIN artist_album aa ON r.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id
WHERE t.album_id = 25
ORDER BY track_position;
~~~

Результатом будет:

![](/pics/korn_issues_result.jpg)
  
Но такой способ очень медленный.
С помощью API [Discogs](https://www.discogs.com/) я смог получить данные о любом альбоме и сохранить их в *json-файл*.
А далее написал скрипт для чтения этого файла и заливки всех данных в базу.
Код находится в файле *add_album_to_database.py*
  
Правда, по ходу работы с *Discogs* обнаружилось несколько нюансов из-за которых не каждый альбом удалось проиндексировать и сохранить.
Но для текущей задачи с запросами этого хватит.
  
Создадим сборник из уже имеющихся в базе треков.
Например, мы хотим создать жанровый сборник из хитов в стиле *Death Metal*.
Создадим сам сборник:

~~~
INSERT INTO compilations (compilation_name, year)
VALUES ('Master of Brutality: Classic of Death Metal', 1999);
~~~

И добавим записи в связующую таблицу *compilation_track*, где 4 это __id__ сборника:

~~~
INSERT INTO compilation_track
VALUES (4, 1045), (4, 1056), (4, 1586), (4, 1605), 
(4, 1658), (4, 1654), (4, 1708), (4, 1736), 
(4, 1777), (4, 1788), (4, 1833), (4, 1832),
(4, 1857), (4, 1876), (4, 1897), (4, 1914);
~~~

Выведем результат с помощью __SELECT__ запроса:

~~~
SELECT artist_name, track_name, duration
FROM tracks t 
JOIN compilation_track ct ON t.id = ct.track_id
JOIN albums ab ON t.album_id = ab.id
JOIN artist_album aa ON ab.id = aa.album_id 
JOIN artists ar ON aa.artist_id = ar.id 
WHERE ct.compilation_id = 4;
~~~

![](/pics/select_comp_result.jpg)

Все запросы в файле *insert_md_data.sql*
  
### 3. __SELECT__ запросы для выборки данных:

> Название и год выхода альбомов, вышедших в 2018 году:

~~~
SELECT album_name, year 
FROM albums
WHERE YEAR = 2018;
~~~

![](/pics/select_result_1.jpg)

> Название и продолжительность самого длительного трека:

~~~
SELECT track_name, duration
FROM tracks
WHERE duration = (SELECT MAX(duration) FROM tracks);
~~~

![](/pics/select_result_2.jpg)

> Название треков, продолжительность которых не менее 3,5 минуты:

~~~
SELECT track_name, duration
FROM tracks
WHERE duration > (3 * 60) + 30;
~~~

![](/pics/select_result_3.jpg)
*Результатом было более 200 записей, на скриншоте первые 10.*

> Названия сборников, вышедших в период с 2018 по 2020 год включительно:

~~~
SELECT compilation_name, year
FROM compilations
WHERE YEAR BETWEEN 2018 AND 2020;
~~~

![](/pics/select_result_4.jpg)

> Исполнители, чье имя состоит из 1 слова:

~~~
SELECT artist_name
FROM artists
WHERE artist_name NOT LIKE '% %';
~~~

![](/pics/select_result_5.jpg)

> Название треков, которые содержат слово "мой"/"my":

~~~
SELECT track_name
FROM tracks
WHERE track_name ILIKE '%my%';
~~~

![](/pics/select_result_6.jpg)

Все запросы в файле *select_md.sql*