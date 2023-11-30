# proteauns-music-streaming-app

# Inspiration
The inspiration behind Proteauns stemmed from our collective passion for music and the desire to create a seamless, user-friendly music streaming experience. We envisioned a platform that integrates popular music databases like Spotify and Musixmatch and adds a unique touch to the user interface for a personalized feel.

# What it does
Proteauns is a Flask-based Music Streaming app that combines the power of Spotify and Musixmatch APIs to offer users a comprehensive music discovery and playback solution. The UI, crafted with Bootstrap, provides an intuitive and visually appealing experience. Users can explore, discover, and enjoy their favourite tunes with the bonus of lyrics provided by Musixmatch.

# How we built it
The foundation of Proteauns lies in Flask, the robust backend that seamlessly integrates with the Spotify API for music catalogue access and playback functionalities. Bootstrap was employed to meticulously design the user interface meticulously, ensuring a responsive and aesthetically pleasing layout.

# Challenges we ran into
Our challenges during development ranged from API authentication intricacies to ensuring a smooth interaction between the frontend and backend components. UWSGI authentication added an extra layer of complexity, requiring careful implementation to secure the application. We wished to implement three blueprints for general_user, admin, and creator. The codebase soon became large and complex to handle just for the two of us. We implemented the general_user route with all the planned features.

> "We wished to implement three blueprints for general_user, admin, and creator. The codebase soon became large and complex to handle just for the two of us."

#Accomplishments that we're proud of
We take pride in achieving a harmonious fusion of functionality and aesthetics in Proteauns. Overcoming the challenges presented by API integrations and authentication mechanisms has resulted in a robust music streaming app. The accomplishment lies not only in the technical aspects but also in creating an application that resonates with users on both a functional and visual level.

# What we learned
We learned how backend-intensive web apps are made using Flask. We learned about how blueprints are used to design our routes. Bootstrap integration helped us understand how to read documentation and also helped us improve our UI/UX skills. Integrating APIs is considered an arduous task, but we took the challenge and realised it is straightforward and fun! Below code snippets demonstrate how we leveraged the Spotify API and Musixmatch API:

> SPOTIFY API INTEGRATION
# Sample code for Spotify API integration in Flask
```
from flask import Flask, request
import requests

app = Flask(__name__)

@app.route('/spotify_search')
def spotify_search():
    query = request.args.get('query')
    response = requests.get(f'https://api.spotify.com/v1/search?q={query}&type=track')
    data = response.json()
    return data
```
Returns:
```
{
  "tracks": {
    "items": [
      {
        "name": "Sample Track",
        "artists": [
          {
            "name": "Sample Artist"
          }
        ],
        "album": {
          "name": "Sample Album"
        },
        "preview_url": "sample_preview_url",
        "external_urls": {
          "spotify": "sample_spotify_url"
        }
      }
    ]
  }
}
```
```
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
```
Returns:
```
{
  "message": {
    "body": {
      "lyrics": {
        "lyrics_body": "Sample lyrics text"
      }
    }
  }
}
```
# What's next for Proteauns
Looking ahead, Proteauns is poised for further enhancements. We wish to complete the remaining routes, namely, the admin and creator routes. For the admin and creator routes, we wish to integrate graphical analysis for their engagement and listener statistics. For the general_user route, we plan on giving them analysis, blends of their music taste, and listening stats. We plan to implement additional features such as personalized playlists, social sharing capabilities, and an expanded catalogue. User feedback will be invaluable in shaping the future of Proteauns, as we strive to create a music streaming platform that meets and exceeds user expectations.


# References
Flask Documentation
Bootstrap Documentation
Spotify API Documentation
Musixmatch API Documentation
