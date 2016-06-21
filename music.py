import spotipy
import json
import urllib2
import json

from spotipy import oauth2



#preview_url = 'https://p.scdn.co/mp3-preview/917c8004b63d09a26021d0d7d9c3db1601be858d'

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
    	results = self.api.search(q=name, limit=1)
    	if len(results['tracks']['items']) <= 0:
    		return {}
    	song = results['tracks']['items'][0]
    	id = song['id']
    	features = self.api.audio_features(tracks=[id])
    	song['features'] = features[0]

    	with open('data.json', 'a') as outfile:
			json.dump(song, outfile, indent=4)

    	return song

   	def download_song(self, url, filename):
   		response = urllib2.urlopen(url)
   		CHUNK = 16 * 1024
		with open(filename, 'wb') as f:
		   while True:
		      chunk = response.read(CHUNK)
		      if not chunk: break
		      f.write(chunk)

