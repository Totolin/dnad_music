import mongo
import utils
from bson.json_util import dumps
from bson.json_util import loads


class Analyzer:

    def __init__(self, manager):
        self.dtb_manager = manager
        self.number = 5;

    def recommend(self, song):
        # Received a song to analyze
        # Should return 5 recommended songs

        # Get the features ofthe song
        # features = song.features
        to_return = []

        search = utils.read_searchConfig()

        for i in search:
            if i == "loudness":
                self.loudness_query(i, search[i], song[i])
            elif i == "tempo":
                self.tempo_query(i, search[i], song[i])
            else:
                self.other_query(i, search[i], song[i])

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

        for index in range(0, self.number):
            to_return.append(to_sort[index])

        return to_return

    def extract_counter(self, json):
        try:
            return json["counter"]
        except KeyError:
            return 0

    def other_query(self, query_name, content, val):
        name = "features." + query_name
        # print (name)
        if content["value"] > val:
            content["array"] = loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                    {
                        name: {
                            "$gte": 0
                        }
                    },
                    {
                        name : {
                            "$lte": 2 * content["value"]
                        }
                    }]
                }
            )))
        elif 1 - content["value"] < val:
            content["array"]= loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                    {
                        name: {
                            "$gte": 1 - 2 * content["value"]
                        }
                    },
                    {
                        name : {
                            "$lte": 1.0
                        }
                    }]
                }
            )))
        else:
            content["array"] = loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                        {
                            name: {
                                "$gte": val - content["value"]
                            }
                        },
                        {
                            name: {
                                "$lte": val + content["value"]
                            }
                        }]
                }
            )))
        # print content["array"]

    def tempo_query(self, query_name, content, val):
        name = "features." + query_name
        # print (name)
        content["array"] = loads(dumps(self.dtb_manager.find(
            {
                "$and": [
                    {
                        name: {
                            "$gte": val - content["value"]
                        }
                    },
                    {
                        name: {
                            "$lte": val + content["value"]
                        }
                    }]
            }
        )))
        # print content["array"]

    def loudness_query(self, query_name, content, val):
        name = "features." + query_name
        # print (name)
        if content["value"] < val:
            content["array"] = loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                        {
                            name: {
                                "$gte": 2 * content["value"]
                            }
                        },
                        {
                            name: {
                                "$lte": 0
                            }
                        }]
                }
            )))
        elif -60 - content["value"] > val:
            content["array"] = loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                        {
                            name: {
                                "$gte": -60
                            }
                        },
                        {
                            name: {
                                "$lte": -60 + 2 * content["value"]
                            }
                        }]
                }
            )))
        else:
            content["array"] = loads(dumps(self.dtb_manager.find(
                {
                    "$and": [
                        {
                            name: {
                                "$gte": val - content["value"]
                            }
                        },
                        {
                            name: {
                                "$lte": val + content["value"]
                            }
                        }]
                }
            )))
        # print content["array"]

'''
mongo = mongo.Mongo("localhost", 27017, "local", "songs")
analyzer = Analyzer(mongo)

analyzer.recommend({ "key" : 10, "analysis_url" : "https://api.spotify.com/v1/audio-analysis/0OF184vEASwoN9x3HTFCPQ", "energy" : 0.676, "liveness" : 0.316, "tempo" : 173.922, "speechiness" : 0.154, "uri" : "spotify:track:0OF184vEASwoN9x3HTFCPQ", "acousticness" : 0.282, "danceability" : 0.69, "track_href" : "https://api.spotify.com/v1/tracks/0OF184vEASwoN9x3HTFCPQ", "time_signature" : 4, "duration_ms" : 205421, "loudness" : -3.874, "mode" : 1, "valence" : 0.392, "type" : "audio_features", "id" : "0OF184vEASwoN9x3HTFCPQ", "instrumentalness" : 0 })
'''


