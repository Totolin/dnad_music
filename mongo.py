import pymongo
from pymongo import MongoClient

class Mongo:

    def __init__(self, url, port, dtb, coll):
        self.url = url
        self.port = port
        self.client = MongoClient(url, port)
        self.db = self.client[dtb]
        self.collection = self.db[coll]

    def set_dtb(self, name):
        self.db = self.client[name]

    def set_collection(self, name):
        self.collection = self.db[name]

    def insert(self, post):
        return self.collection.insert_one(post)

    def find(self, query):
        return self.collection.find(query)