## Музыкальная база

Создание таблиц для жанров, исполнителей, альбомов и композиций:

```
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
```
В таблицу с композициями я решил еще добавить атрибут __track_position__, т.к. в рамках альбома у каждой композиции есть свой порядковый номер.
  
Добавление дополнительных таблиц со связями:

```
CREATE TABLE artist_genre(
	artist_id INTEGER REFERENCES artists(id),
	genre_id INTEGER REFERENCES genres(id),
	CONSTRAINT art_gen PRIMARY KEY (artist_id, genre_id)
);
```
То есть в таблице __artist_genre__ будет связь исполнителя и жанра, так как один и тот же исполнитель может играть в разных жанрах.
И в одном жанре, в свою очередь, могут играть множество исполнителей.
Ключем в этой таблице будет сочетание __id__ исполнителей и жанров.


```
CREATE TABLE artist_album(
	artist_id INTEGER REFERENCES artists(id),
	album_id INTEGER REFERENCES albums(id),
	CONSTRAINT art_alb PRIMARY KEY (artist_id, album_id)
);
```

Аналогичная таблица для связи исполнителей и альбомов, так как один альбом могут выпустить совместно несколько исполнителей.
И один исполнитель может выпустить несколько альбомов.
  

>С треками ничего не меняем, все так же трек принадлежит строго одному альбому.
>Но появилась новая сущность - сборник. Сборник имеет название и год выпуска. В него входят различные треки из разных альбомов.
>Обратите внимание: один и тот же трек может присутствовать в разных сборниках.
  
Не уверен, что правильно понял часть задания про сборники.
Для сборников я создал отдельную таблицу, которая имеет связь с __id__ композицией из таблицы __tracks__.
Т.е. в одном сборнике может быть несколько композиций, которые имеют связь с другими альбомами.
При этом в таблице __tracks__ каждая композиция остается уникальной и имеет связь с конкретным альбомом.
  
Но, как мне кажется, отдельная таблица для сборников особо не нужна.
Ведь можно между альбомами и треками использовать аналогичную таблицу связей как с __artist_genre__ или __artist_album__.
А в альбомы можно еще добавить тип (например EP, single или тот же сборник).
И уже в таблице связи определять какая композиция какому альбому принадлежит.

```
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
```
    
В итоге схема музыкальной базы данных выглядит вот так:

![](/music_base_scheme.jpg)