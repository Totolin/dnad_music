import json
from music import SpotifyConnect
from reader import SongsReader
from mongo import Mongo
from research import Researcher
from analyzer import Analyzer
import communication
import utils
import threading
import time
from multiprocessing import Process

song = {"album" : { "album_type" : "album", "name" : "My World 2.0", "external_urls" : { "spotify" : "https://open.spotify.com/album/3BmcYMh0KYsimWL6p2gPa9" }, "uri" : "spotify:album:3BmcYMh0KYsimWL6p2gPa9", "href" : "https://api.spotify.com/v1/albums/3BmcYMh0KYsimWL6p2gPa9", "images" : [ { "url" : "https://i.scdn.co/image/ebc4de0afdb9d3126dea124538f5a7479fcac70b", "width" : 640, "height" : 640 }, { "url" : "https://i.scdn.co/image/24f1de6be0489bac031381df29ad3512d80cb4ef", "width" : 300, "height" : 300 }, { "url" : "https://i.scdn.co/image/5eaa3d2e49e629a1b24293ffd0bd75bbd83481df", "width" : 64, "height" : 64 } ], "type" : "album", "id" : "3BmcYMh0KYsimWL6p2gPa9", "available_markets" : [ "CA", "US" ] }, "name" : "Baby", "external_urls" : { "spotify" : "https://open.spotify.com/track/6epn3r7S14KUqlReYr77hA" }, "popularity" : 64, "uri" : "spotify:track:6epn3r7S14KUqlReYr77hA", "preview_url" : "https://p.scdn.co/mp3-preview/a7457c94f24ced0115c865b325e031ea6fb2a964", "disc_number" : 1, "href" : "https://api.spotify.com/v1/tracks/6epn3r7S14KUqlReYr77hA", "artists" : [ { "name" : "Justin Bieber", "external_urls" : { "spotify" : "https://open.spotify.com/artist/1uNFoZAHBGtllmzznpCI3s" }, "uri" : "spotify:artist:1uNFoZAHBGtllmzznpCI3s", "href" : "https://api.spotify.com/v1/artists/1uNFoZAHBGtllmzznpCI3s", "type" : "artist", "id" : "1uNFoZAHBGtllmzznpCI3s" }, { "name" : "Ludacris", "external_urls" : { "spotify" : "https://open.spotify.com/artist/3ipn9JLAPI5GUEo4y4jcoi" }, "uri" : "spotify:artist:3ipn9JLAPI5GUEo4y4jcoi", "href" : "https://api.spotify.com/v1/artists/3ipn9JLAPI5GUEo4y4jcoi", "type" : "artist", "id" : "3ipn9JLAPI5GUEo4y4jcoi" } ], "duration_ms" : 214240, "external_ids" : { "isrc" : "USUM70919263" }, "track_number" : 1, "type" : "track", "id" : "6epn3r7S14KUqlReYr77hA", "available_markets" : [ "CA", "US" ], "features" : { "key" : 5, "analysis_url" : "https://api.spotify.com/v1/audio-analysis/6epn3r7S14KUqlReYr77hA", "energy" : 0.841, "liveness" : 0.122, "tempo" : 65.024, "speechiness" : 0.232, "uri" : "spotify:track:6epn3r7S14KUqlReYr77hA", "acousticness" : 0.0544, "danceability" : 0.656, "track_href" : "https://api.spotify.com/v1/tracks/6epn3r7S14KUqlReYr77hA", "time_signature" : 4, "duration_ms" : 214240, "loudness" : -5.183, "mode" : 0, "valence" : 0.519, "type" : "audio_features", "id" : "6epn3r7S14KUqlReYr77hA", "instrumentalness" : 0 } }

config = utils.read_config()
if __name__ == '__main__':
    
    # Get the reader. Will use it to read all our songs
    reader = SongsReader(
        config["files"]["songs"],
        config["wordlist"],
        None
    )

    # Create a database manager
    mongo = Mongo(
        config["mongo"]["url"],
        config["mongo"]["port"],
        config["mongo"]["database"],
        config["mongo"]["collection"]
    )

    # Create a Spotify Caller
    spotify = SpotifyConnect(
        config["spotify"]["client_id"],
        config["spotify"]["client_secret"]
    )

    # Create a music researcher (grab songs from the internet)
    researcher = Researcher(reader, spotify, mongo)
    res_proc = Process(target=researcher.start)
    res_proc.start()

    # Create a music analyzer
    #analyzer = Analyzer(mongo, spotify, config["search"])
    #songs = analyzer.recommend(song)
    #utils.pretty_print(songs)

    # Create the communication API for the WebServer
    #app = communication.create(analyzer)
    #api = Process(target=app.run)
    #api.start()

    # Exit code
    try:
        while 1:
            time.sleep(.1)
    except KeyboardInterrupt:
        api.terminate()
        api.join()
        res_proc.terminate()
        res_proc.join()
        print "Processes successfully closed"