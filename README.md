## Музыкальная база

Создадим таблицы для жанров, исполнителей, альбомов и композиций:

```
CREATE TABLE genres(
	id SERIAL PRIMARY KEY,
	genre_name VARCHAR(100) NOT NULL
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
	track_name VARCHAR(100) NOT NULL,
	duration INTEGER NOT NULL,
	album_id INTEGER NOT NULL REFERENCES albums(id)
);
```


Добавим дополнительные таблицы со связями:

```
CREATE TABLE artist_genre(
	artist_id INTEGER REFERENCES artists(id),
	genre_id INTEGER REFERENCES genres(id),
	CONSTRAINT art_gen PRIMARY KEY (artist_id, genre_id)
);
```

То есть в таблице __artist_genre__ будет связть исполнителя и жанра, так как один и тот же исполнитель, может играть в разных жанрах. И в одном жанре, в свою очередь, могут играть множество исполнителей. Ключем в этой таблице будет сочетание __id__ исполнителей и жанров.


```
CREATE TABLE artist_album(
	artist_id INTEGER REFERENCES artists(id),
	album_id INTEGER REFERENCES albums(id),
	CONSTRAINT art_alb PRIMARY KEY (artist_id, album_id)
);
```

Аналогичная таблица для связи исполнителей и альбомов, так как один альбом могут выпустить несколько исполнителей. И один исполнитель может выпустить несколько альбомов.


```
CREATE TABLE compilations(
	id SERIAL PRIMARY KEY,
	compilation_name VARCHAR(100) NOT NULL,
	year INTEGER NOT NULL,
	track_id INTEGER REFERENCES tracks(id)
);
```

Не уверен, что правильно понял часть задания про сборники. Для сборников я создал отдельную таблицу, которая имеет связь с id композицией из таблицы tracks. Т.е. в одном сборнике может быть несколько композиций, которые имеют связь с другими альбомами. При этом в таблице tracks каждая композиция остается уникальной и имеет.
Но тогда, как мне кажется, проще использовать аналогичную таблицу связей как с __artist_genre__ или __artist_album__. То есть в таблице __album_track__ можно будет добавить, что одна и та же композиция может быть во многих альбомах и альбом может иметь несколько композиций.


```
CREATE TABLE artist_track(
	artist_id INTEGER REFERENCES artists(id),
	track_id INTEGER REFERENCES tracks(id),
	CONSTRAINT art_trck PRIMARY KEY (artist_id, track_id)
);
```

По такому же принципу я решил добавить связь композиций и исполнителей. Если делать запрос на то, чтобы узнать у какого исполнителя какие композиции, то через __JOIN__ придется склеивать и __albums__, и таблицы связей между ними. Это сделает запрос во-первых - слишком большим, а во-вторых - нам не нужна информация об альбомах.
Одну и ту же композицию могут выпустить несколько совместно несколько исполнителей. Правда одна и та же композиция не может принадлежать разным исполнителям. Поэтому насчет таблицы artist_track я неуверен.