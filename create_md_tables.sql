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