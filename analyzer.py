import mongo
import utils
from bson.json_util import dumps
from bson.json_util import loads
import math
from sets import Set

class Analyzer:

    def __init__(self, manager, spotify, config):
        self.dtb_manager = manager
        self.spotify = spotify
        self.number = 5;
        self.search = config

    # Received a song to analyze
    # Should return 5 recommended songs
    def recommend(self, name):

        # We only received the song name. Tell spotify to give us the data
        song = self.spotify.get_song(name)

        # It's possible Spotify doesn't know that song
        if song is None or len(song) < 2:
            return []

        # Get the song's features
        features = song["features"]
        to_return = []

        # Get all songs according to intervals
        for i in self.search:
            if i == "loudness":
                self.loudness_query(i, self.search[i], features[i])
            elif i == "tempo":
                self.tempo_query(i, self.search[i], features[i])
            else:
                self.other_query(i, self.search[i], features[i])

        counter = {}
        to_sort = []

        # Give a score to each song by the number of occurences
        for i in self.search:
            for songs in self.search[i]["array"]:
                if songs["id"] != song["id"]:
                    if songs["id"] in counter.keys():
                        counter[songs["id"]] += 1
                    else:
                        counter[songs["id"]] = 1

        # Recreate the array for easy use
        for count in counter.keys():
            to_sort.append({"id" : count, "counter" : counter[count]})

        # Sort items by highest matching score based on intervals
        to_sort.sort(key=self.extract_counter, reverse=True)

        # Extract only top 100 relevant songs
        relevant = to_sort[:100]

        return self.top_songs(song, relevant, 5)

    def extract_counter(self, json):
        try:
            return json["counter"]
        except KeyError:
            return 0

    def other_query(self, query_name, content, val):
        name = "features." + query_name
        if content["value"] > val:
            self.queryBetween(2 * content["value"], 0, name, content)
        elif 1 - content["value"] < val:
            self.queryBetween(1.0, 1 - 2 * content["value"], name, content)
        else:
            self.queryBetween(val + content["value"], val - content["value"], name, content)

    def tempo_query(self, query_name, content, val):
        name = "features." + query_name
        self.queryBetween(val + content["value"], val - content["value"], name, content)

    def loudness_query(self, query_name, content, val):
        name = "features." + query_name
        if content["value"] < val:
            self.queryBetween(0, 2 * content["value"], name, content)
        elif -60 - content["value"] > val:
            self.queryBetween(-60 + 2 * content["value"], -60, name, content)
        else:
            self.queryBetween(val + content["value"], val - content["value"], name, content)

    def queryBetween(self, lte, gte, name, content):
        content["array"] = loads(dumps(self.dtb_manager.find(
            {
                "$and": [
                    {
                        name: {
                            "$gte": gte
                        }
                    },
                    {
                        name: {
                            "$lte": lte
                        }
                    }]
            }
        )))

    def pearson(self, x, y,length):
        if None in x or None in y:
            return 0

        upper_left = 0 # length * sum(Xi * Yi)

        x_sum = 0
        y_sum = 0
        x_pow_sum = 0
        y_pow_sum = 0

        for i in range(0, length):
            upper_left += x[i] * y[i]
            x_sum += x[i]
            y_sum += y[i]

            x_pow_sum += math.pow(x[i], 2)
            y_pow_sum += math.pow(y[i], 2)

        upper_left *= length
        upper_right = x_sum * y_sum # sum(Xi) * sum(Yi)
        lower_left = math.sqrt(length * x_pow_sum - math.pow(x_sum, 2)) # sqrt(length * sum(Xi ^ 2) - sum(Xi) ^ 2)
        lower_right = math.sqrt(length * y_pow_sum - math.pow(y_sum, 2)) # sqrt(length * sum(Yi ^ 2) - sum(Yi) ^ 2)

        return (upper_left - upper_right) / (lower_left * lower_right)

    def top_songs(self, song, songs_ids, length):
        song_array = []
        self.append_features(song_array, song["features"])

        songs = []

        for i in range(0, length):
            songs.extend(loads(dumps(self.dtb_manager.find({"id": songs_ids[i]["id"]}))))

        for i in range(0, length):
            compare_array = []
            self.append_features(compare_array, songs[i]["features"])
            songs[i]["pearson"] = self.pearson(song_array, compare_array, 8)

        songs.sort(key=self.extract_pearson, reverse=True)

        return songs

    def extract_pearson(self, json):
        try:
            return json["pearson"]
        except KeyError:
            return 0

    def append_features(self, array, features):
        array.append(features["acousticness"])
        array.append(features["danceability"])
        array.append(features["energy"])
        array.append(features["instrumentalness"])
        array.append(features["loudness"])
        array.append(features["speechiness"])
        array.append(features["tempo"])
        array.append(features["valence"])



