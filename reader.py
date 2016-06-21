import json

class SongsReader:

    def __init__(self, path, previous):
        self.songs_path = path
        self.content = self.read()

        if (previous == None):
        	self.index = 0
        else:
        	self.index = previous

    def read(self):
    	songs = []
    	with open(self.songs_path, "r") as ins:
    		for line in ins:
        		# Split each line by it's separator
        		parts = line.split("<SEP>")

        		# Create the song dict
        		song = {}
        		song['track_id'] = parts[0]
        		song['song_id']  = parts[1]
        		song['artist'] = parts[2]
        		song['title'] = parts[3].strip('\n')

        		songs.append(song)

        return songs
 
    def next(self):
    	song = self.content[self.index]
    	self.index+=1
    	return song


#reader = SongsReader('unique_tracks.txt', None)




