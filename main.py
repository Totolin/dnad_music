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



config = utils.read_config()
if __name__ == '__main__':
    
    # Get the reader. Will use it to read all our songs
    reader = SongsReader(config["files"]["songs"], None)

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
    #res_proc = Process(target=researcher.start)
    #res_proc.start()

    # Create a music analyzer
    analyzer = Analyzer(mongo)
    result = analyzer.recommend({ "key" : 10, "analysis_url" : "https://api.spotify.com/v1/audio-analysis/0OF184vEASwoN9x3HTFCPQ", "energy" : 0.676, "liveness" : 0.316, "tempo" : 173.922, "speechiness" : 0.154, "uri" : "spotify:track:0OF184vEASwoN9x3HTFCPQ", "acousticness" : 0.282, "danceability" : 0.69, "track_href" : "https://api.spotify.com/v1/tracks/0OF184vEASwoN9x3HTFCPQ", "time_signature" : 4, "duration_ms" : 205421, "loudness" : -3.874, "mode" : 1, "valence" : 0.392, "type" : "audio_features", "id" : "0OF184vEASwoN9x3HTFCPQ", "instrumentalness" : 0 })
    utils.pretty_print(result)

    # Create the communication API for the WebServer
    #app = communication.create()
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