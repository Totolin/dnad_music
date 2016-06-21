import json
from music import SpotifyConnect
from reader import SongsReader
from mongo import Mongo
from research import Researcher
from analyzer import Analyzer
import utils


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

	# Create a music analyzer
	analyzer = Analyzer(mongo)

	# Create a Spotify Caller
	spotify = SpotifyConnect(
		config["spotify"]["client_id"],
		config["spotify"]["client_secret"]
	)

	# Create a music researcher (grab songs from the internet)
	researcher = Researcher(reader, spotify, mongo)
	researcher.create()