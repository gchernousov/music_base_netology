INSERT INTO artists (artist_name)
VALUES ('Korn');

INSERT INTO genres (genre_name)
VALUES ('Nu Metal');

INSERT INTO artist_genre VALUES (49, 27);

INSERT INTO albums (album_name, year)
VALUES ('Issues', 1999);

INSERT INTO artist_album VALUES (49, 25);

INSERT INTO tracks (track_name, duration, album_id, track_position)
VALUES ('Falling Away From Me', 270, 25, 2);

INSERT INTO compilations (compilation_name, year)
VALUES ('Master of Brutality: Classic of Death Metal', 1999);

INSERT INTO compilation_track
VALUES (4, 1045), (4, 1056), (4, 1586), (4, 1605), 
(4, 1658), (4, 1654), (4, 1708), (4, 1736), 
(4, 1777), (4, 1788), (4, 1833), (4, 1832),
(4, 1857), (4, 1876), (4, 1897), (4, 1914);