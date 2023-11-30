from flask import Blueprint, render_template, redirect, url_for, session, request, flash, g
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from app.db import get_db
import requests
from app.auth import login_required


bp = Blueprint('general', __name__, url_prefix='/general')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM users WHERE user_id = ?', (user_id,)
        ).fetchone()


# Spotify API credentials
SPOTIPY_CLIENT_ID = '6d02dba60a604bf2bd25167569db3a84'
SPOTIPY_CLIENT_SECRET = '29ae099284b648689275942c01a912f4'
SPOTIPY_REDIRECT_URI = 'http://localhost:5000'

#MusixMatch API creds
MM_API_KEY = 'be8161ea98a6a3c181428f7faa75dd7e'

client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

playlist_link = "https://open.spotify.com/playlist/37i9dQZEVXbNG2KDcFcKOF?si=1333723a6eff4b7f"
playlist_URI = playlist_link.split("/")[-1].split("?")[0]
track_uris = [x["track"]["uri"] for x in sp.playlist_tracks(playlist_URI)["items"]]

details = []

def get_track_info(track_name, artist_name):
    # You can implement logic to fetch track name and artist from Spotify or your data source
    # For simplicity, we'll use a static dictionary
    track_info = {
        'name': track_name,
        'artist': artist_name,
    }
    return track_info



def fetch_lyrics(track_info):
    track_name = track_info['name']
    artist_name = track_info['artist']

    # Musixmatch API endpoint for track lyrics
    endpoint = f'https://api.musixmatch.com/ws/1.1/matcher.lyrics.get'

    # Define the request parameters
    params = {
        'q_track': track_name,
        'q_artist': artist_name,
        'apikey': MM_API_KEY,
    }

    # Make the API request
    response = requests.get(endpoint, params=params)
    data = response.json()

    # Check if lyrics were found
    if 'message' in data and 'body' in data['message']:
        lyrics = data['message']['body']['lyrics']['lyrics_body']
        return lyrics
    else:
        return None

limit = 3
for track in sp.playlist_tracks(playlist_URI)["items"]:
    #URI
    track_uri = track["track"]["uri"]
    
    #Track name
    track_name = track["track"]["name"]
    
    #Main Artist
    artist_uri = track["track"]["artists"][0]["uri"]
    artist_info = sp.artist(artist_uri)
    
    #Name, popularity, genre
    artist_name = track["track"]["artists"][0]["name"]
    artist_pop = artist_info["popularity"]
    artist_genres = artist_info["genres"]
    
    #Album
    album = track["track"]["album"]["name"]
    
    #Popularity of the track
    track_pop = track["track"]["popularity"]
    
    #track id
    track_id = track["track"]["id"]

    if limit > 0:
        track_info = get_track_info(track_name, artist_name)
        lyrics = fetch_lyrics(track_info)
        limit = limit - 1

    d = [track_uri, track_name, artist_uri, artist_info, artist_name, artist_pop, artist_genres, album, track_pop, lyrics, track_id]
    details.append(d)

# print(details[0][0])


@bp.route('/user_dashboard')
def user_dashboard():
    return render_template('general/user_dashboard.html')

@bp.route('/view_songs')
def view_songs():
    return render_template('general/view_songs.html', details = details)

@bp.route('/read_lyrics/<int:song_id>')
def read_lyrics(song_id):
    # Fetch and display lyrics of the selected song from your database
    # Implement this logic based on your database structure
    return render_template('general/read_lyrics.html')

@bp.route('/create_playlist', methods=['GET', 'POST'])
def create_playlist():
    # Implement playlist creation form and logic
    return render_template('general/create_playlist.html')


@bp.route('/rate_song/<string:song_id>', methods=['POST'])
def rate_song(song_id):
    load_logged_in_user()
    # Implement song rating functionality
    if request.method == 'POST':
        rating = int(request.form['rating'])
        
        # Validate the rating (1-5)
        if 1 <= rating <= 5:
            # Save the rating to the database (you may want to add the user_id as well)
            db = get_db()
            db.execute(
                'INSERT INTO ratings (song_id, user_id, rating) VALUES (?, ?, ?)',
                (song_id, g.user, rating)
            )
            db.commit()
            flash('Rating submitted successfully', 'success')
        else:
            flash('Invalid rating. Please choose a rating between 1 and 5.', 'error')
        
        return redirect(url_for('general.view_songs'))
