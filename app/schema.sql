-- Drop existing tables if they exist
DROP TABLE IF EXISTS playlist_songs;
DROP TABLE IF EXISTS playlists;
DROP TABLE IF EXISTS ratings;
DROP TABLE IF EXISTS songs;
DROP TABLE IF EXISTS albums;
DROP TABLE IF EXISTS users;


DROP VIEW IF EXISTS latest_albums;
DROP VIEW IF EXISTS latest_songs;
DROP VIEW IF EXISTS top_rated_songs;

-- Create the users table to store information about app users.
CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    is_admin BOOLEAN NOT NULL DEFAULT false,
    is_creator BOOLEAN NOT NULL DEFAULT false
);

-- Create the albums table to store information about music albums.
CREATE TABLE albums (
    album_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    genre VARCHAR(50),
    artist VARCHAR(100),
    creator_id INT REFERENCES users(user_id)
);

-- Create the songs table to store information about individual songs.
CREATE TABLE songs (
    song_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    lyrics TEXT,
    duration INTERVAL,
    album_id INT REFERENCES albums(album_id)
);

-- Create the ratings table to allow users to rate songs.
CREATE TABLE ratings (
    rating_id SERIAL PRIMARY KEY,
    song_id SERIAl REFERENCES songs(song_id),
    user_id INT REFERENCES users(user_id),
    rating INT CHECK (rating >= 1 AND rating <= 5)
);

-- Create the playlists table to allow users to create and manage playlists.
CREATE TABLE playlists (
    playlist_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    user_id INT REFERENCES users(user_id)
);

-- Create the playlist_songs table to associate songs with playlists.
CREATE TABLE playlist_songs (
    playlist_id INT REFERENCES playlists(playlist_id),
    song_id INT REFERENCES songs(song_id),
    PRIMARY KEY (playlist_id, song_id)
);

-- Create the views
CREATE VIEW latest_albums AS
SELECT album_id, name, genre, artist
FROM albums
ORDER BY album_id DESC;

CREATE VIEW latest_songs AS
SELECT song_id, name, lyrics, duration
FROM songs
ORDER BY song_id DESC;

CREATE VIEW top_rated_songs AS
SELECT s.song_id, s.name, s.lyrics, s.duration, AVG(r.rating) AS average_rating
FROM songs s
LEFT JOIN ratings r ON s.song_id = r.song_id
GROUP BY s.song_id
ORDER BY average_rating DESC;
