import sqlalchemy

import json
from pprint import pprint


engine = sqlalchemy.create_engine('postgresql://admin_music:admin123@localhost:5432/music_base_net')
connection = engine.connect()


def open_album_data():
    """Открытие и чтение json файла с данными об альбоме"""
    file_name = input("What album_file to open?: ")
    dir = "album_datas/" + file_name + '.json'
    with open(dir, encoding="utf-8") as album_file:
        data = json.load(album_file)

    return data


def get_add_genre(g_genres):
    """Добавление жанров в таблицу genres / Результат: список id жанров"""
    id_genres_list = []
    for genre in g_genres:
        query = connection.execute(f"SELECT * FROM genres WHERE genre_name = '{genre}';").fetchone()
        if query == None:
            connection.execute(f"INSERT INTO genres (genre_name) VALUES ('{genre}');")
            print(f'>>> {genre} добавлен в базу...')
            res = connection.execute(f"SELECT * FROM genres ORDER BY id DESC LIMIT (1);").fetchone()
            genre_id = res[0]
        else:
            print(f'>>> {genre} уже есть в базе...')
            genre_id = query[0]
        id_genres_list.append(genre_id)

    return id_genres_list


def get_add_artist(g_artist_name):
    """Добавление исполнителя в таблицу artist / Результат: id исполнителя"""
    query = connection.execute(f"SELECT * FROM artists WHERE artist_name = '{g_artist_name}';").fetchone()
    if query == None:
        connection.execute(f"INSERT INTO artists (artist_name) VALUES ('{g_artist_name}');")
        print(f'>>> {g_artist_name} добавлен в базу...')
        res = connection.execute(f"SELECT * FROM artists ORDER BY id DESC LIMIT (1);").fetchone()
        id_artist = res[0]
    else:
        print(f'>>> {g_artist_name} уже есть в базе...')
        id_artist = query[0]

    return id_artist


def add_connection_artist_genre(id_artist, id_genres_list):
    """Добавление связи id исполнителя и id жанра в таблицу artist_genre"""
    for id_genre in id_genres_list:
        query = connection.execute(f"""
            SELECT * FROM artist_genre
            WHERE artist_id = {id_artist} AND genre_id = {id_genre};
            """).fetchone()
        if query == None:
            connection.execute(f"INSERT INTO artist_genre VALUES ({id_artist}, {id_genre});")
            print('>>> Связь ARTIST = GENRE добавлена...')
        else:
            print('>>> Связь ARTIST = GENRE уже есть в базе...')


def insert_album(g_album_title, g_year):
    """Добавление альбома в таблицу albums / Результат: id альбома"""
    connection.execute(f"""
        INSERT INTO albums (album_name, year)
        VALUES ('{g_album_title}', {g_year});
        """)
    query = connection.execute(f"SELECT * FROM albums ORDER BY id DESC LIMIT (1);").fetchone()
    id_album = query[0]
    return id_album


def get_add_album(g_album_title, g_year, id_artist):
    """Проверка наличия альбома в базе."""
    # Проверка происходит по запросу в таблицу связей альбома и исполнителя.
    # Ищем наличие альбома по его названию у исполнителя по его ID.
    query = connection.execute(f"""
        SELECT * FROM artist_album 
        WHERE artist_id = {id_artist};
        """).fetchall()
    if query == []:
        id_album = insert_album(g_album_title, g_year)
        print(f'>>> Альбом {g_album_title} добавлен в базу...')
    else:
        album_name_list = []
        query = connection.execute(f"""
        SELECT id, album_name FROM albums a
        JOIN artist_album aa ON a.id = aa.album_id
        WHERE artist_id = {id_artist};
        """).fetchall()
        for album in query:
            album_name_list.append(album[1])
        if g_album_title in album_name_list:
            print(f'>>> Альбом {g_album_title} уже есть в базе...')
            q = connection.execute(f"SELECT * FROM artist_album WHERE artist_id = '{id_artist}';").fetchone()
            id_album = q[1]
        else:
            id_album = insert_album(g_album_title, g_year)
            print(f'>>> Альбом {g_album_title} добавлен в базу...')

    return id_album


def add_connection_artist_album(id_album, id_artist):
    """Добавление связи id альбома и id исполнителя в таблицу artist_album"""
    query = connection.execute(f"""
        SELECT * FROM artist_album
        WHERE artist_id = {id_artist} AND album_id = {id_album};
        """).fetchone()
    if query == None:
        connection.execute(f"INSERT INTO artist_album VALUES ({id_artist}, {id_album});")
        print('>>> Связь ARTIST = ALBUM добавлена...')
    else:
        print('>>> Связь ARTIST = ALBUM уже есть в базе...')


def get_add_tracks(g_tracklist, id_album):
    """Добавление композиций в таблицу tracks."""
    # Перед добавлением проверяем, есть ли у нужного альбома уже какие-либо композиции
    query = connection.execute(f"SELECT * FROM tracks WHERE album_id = {id_album};").fetchall()
    if query == []:
        for track in g_tracklist:
            connection.execute(f"""
            INSERT INTO tracks (track_name, duration, album_id, track_position)
            VALUES ('{track['title']}', {track['duration']}, {id_album}, {track['position']});
            """)
        print('>>> Композиции добавлены в базу...')
    else:
        q = connection.execute(f"SELECT * FROM albums WHERE id = {id_album};").fetchone()
        album = q[1]
        print(f'>>> Композиции для альбома {album} уже есть в базе...')


def get_add_all_data(album_data):
    """Полное добавление всей информации об альбоме в базу
    (жанр, исполнитель, альбом, треки + все связи)"""

    # Собираем ключевые данные:
    g_artist_name = album_data["artist_name"]
    g_genres = album_data["genres"]
    g_album_title = album_data["album_title"]
    g_year = album_data["year"]
    g_tracklist = album_data["tracklist"]

    # Добавляем список жанров и исполнителя. Получаем ID жанров и исполнителя:
    id_genres_list = get_add_genre(g_genres)
    id_artist = get_add_artist(g_artist_name)

    # Добавляем связь ID жанра и исполнителя:
    add_connection_artist_genre(id_artist, id_genres_list)

    # Добавляем альбом и получаем его ID:
    id_album = get_add_album(g_album_title, g_year, id_artist)

    # Добавляем связь ID альбома и исполнителя:
    add_connection_artist_album(id_album, id_artist)

    # Добавляем композиции:
    get_add_tracks(g_tracklist, id_album)

    print(f'*** Обработка ({g_artist_name} - {g_year} - {g_album_title}) закончена! ***')


if __name__ == "__main__":

    album_data = open_album_data()
    get_add_all_data(album_data)