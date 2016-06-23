import mongo
import utils
from bson.json_util import dumps
from bson.json_util import loads
import math
from sets import Set

class Analyzer:

    def __init__(self, manager):
        self.dtb_manager = manager
        self.number = 5;

    def recommend(self, song):
        # Received a song to analyze
        # Should return 5 recommended songs

        # Get the features ofthe song
        features = song["features"]
        to_return = []

        search = utils.read_searchConfig()

        for i in search:
            if i == "loudness":
                self.loudness_query(i, search[i], features[i])
            elif i == "tempo":
                self.tempo_query(i, search[i], features[i])
            else:
                self.other_query(i, search[i], features[i])

        counter = {}
        to_sort = []

        for i in search:
            for songs in search[i]["array"]:
                if songs["id"] != song["id"]:
                    if songs["id"] in counter.keys():
                        counter[songs["id"]] += 1
                    else:
                        counter[songs["id"]] = 1

        for count in counter.keys():
            to_sort.append({"id" : count, "counter" : counter[count]})

        to_sort.sort(key=self.extract_counter, reverse=True)

        if len(to_sort) < 100:
            return to_sort
        else:
            for index in range(0, 100):
                to_return.append(to_sort[index])

        return to_return

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
        # print content["array"]

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

mongo = mongo.Mongo("localhost", 27017, "local", "songs")
analyzer = Analyzer(mongo)

song = {"album" : { "album_type" : "album", "name" : "My World 2.0", "external_urls" : { "spotify" : "https://open.spotify.com/album/3BmcYMh0KYsimWL6p2gPa9" }, "uri" : "spotify:album:3BmcYMh0KYsimWL6p2gPa9", "href" : "https://api.spotify.com/v1/albums/3BmcYMh0KYsimWL6p2gPa9", "images" : [ { "url" : "https://i.scdn.co/image/ebc4de0afdb9d3126dea124538f5a7479fcac70b", "width" : 640, "height" : 640 }, { "url" : "https://i.scdn.co/image/24f1de6be0489bac031381df29ad3512d80cb4ef", "width" : 300, "height" : 300 }, { "url" : "https://i.scdn.co/image/5eaa3d2e49e629a1b24293ffd0bd75bbd83481df", "width" : 64, "height" : 64 } ], "type" : "album", "id" : "3BmcYMh0KYsimWL6p2gPa9", "available_markets" : [ "CA", "US" ] }, "name" : "Baby", "external_urls" : { "spotify" : "https://open.spotify.com/track/6epn3r7S14KUqlReYr77hA" }, "popularity" : 64, "uri" : "spotify:track:6epn3r7S14KUqlReYr77hA", "preview_url" : "https://p.scdn.co/mp3-preview/a7457c94f24ced0115c865b325e031ea6fb2a964", "disc_number" : 1, "href" : "https://api.spotify.com/v1/tracks/6epn3r7S14KUqlReYr77hA", "artists" : [ { "name" : "Justin Bieber", "external_urls" : { "spotify" : "https://open.spotify.com/artist/1uNFoZAHBGtllmzznpCI3s" }, "uri" : "spotify:artist:1uNFoZAHBGtllmzznpCI3s", "href" : "https://api.spotify.com/v1/artists/1uNFoZAHBGtllmzznpCI3s", "type" : "artist", "id" : "1uNFoZAHBGtllmzznpCI3s" }, { "name" : "Ludacris", "external_urls" : { "spotify" : "https://open.spotify.com/artist/3ipn9JLAPI5GUEo4y4jcoi" }, "uri" : "spotify:artist:3ipn9JLAPI5GUEo4y4jcoi", "href" : "https://api.spotify.com/v1/artists/3ipn9JLAPI5GUEo4y4jcoi", "type" : "artist", "id" : "3ipn9JLAPI5GUEo4y4jcoi" } ], "duration_ms" : 214240, "external_ids" : { "isrc" : "USUM70919263" }, "track_number" : 1, "type" : "track", "id" : "6epn3r7S14KUqlReYr77hA", "available_markets" : [ "CA", "US" ], "features" : { "key" : 5, "analysis_url" : "https://api.spotify.com/v1/audio-analysis/6epn3r7S14KUqlReYr77hA", "energy" : 0.841, "liveness" : 0.122, "tempo" : 65.024, "speechiness" : 0.232, "uri" : "spotify:track:6epn3r7S14KUqlReYr77hA", "acousticness" : 0.0544, "danceability" : 0.656, "track_href" : "https://api.spotify.com/v1/tracks/6epn3r7S14KUqlReYr77hA", "time_signature" : 4, "duration_ms" : 214240, "loudness" : -5.183, "mode" : 0, "valence" : 0.519, "type" : "audio_features", "id" : "6epn3r7S14KUqlReYr77hA", "instrumentalness" : 0 } }
songs = analyzer.recommend(song)

print analyzer.top_songs(song, songs, len(songs))
