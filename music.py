import spotipy
import json
import urllib2
import json

from spotipy import oauth2

class SpotifyConnect:

    def __init__(self, id, secret):
        self.token = self.login(id,secret)
        self.api = spotipy.Spotify(self.token)

    def login(self,id,secret):
        # Register on AUTH URL
        sp_oauth = oauth2.SpotifyClientCredentials(id,secret)

        # Return the token
        return sp_oauth.get_access_token()

    def get_song(self, name):
        # Get all results from Spotify
        results = self.api.search(q=name, limit=1)

        # Check if we got any
        if len(results['tracks']['items']) <= 0:
            return {}

        # Extract the song we are interested in
        song = results['tracks']['items'][0]

        if (len(song) < 2):
            return {}

        # Get the song's features from Spotify
        id = song['id']
        features = self.api.audio_features(tracks=[id])
        song['features'] = features[0]

        # Convert it's ID to _ID (for uniqueness in mongo)
        song['_id'] = id

        return song

    def get_multiple(self, name):
        # Get all results from Spotify
        results = self.api.search(q=name, limit=19)

        # Check if we got any
        if len(results['tracks']['items']) <= 0:
            return {}

        # Extract the song we are interested in
        songs = results['tracks']['items']

        if (len(songs) < 2):
            return {}

        # Get the song's features from Spotify
        for song in songs:
            id = song['id']
            features = self.api.audio_features(tracks=[id])
            song['features'] = features[0]

            # Convert it's ID to _ID (for uniqueness in mongo)
            song['_id'] = id

        return songs


    def download_song(self, url, filename):
        response = urllib2.urlopen(url)
        CHUNK = 16 * 1024
        with open(filename, 'wb') as f:
           while True:
              chunk = response.read(CHUNK)
              if not chunk: break
              f.write(chunk)

