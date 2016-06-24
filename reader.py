from random import randint

class SongsReader:

    def __init__(self, path, words, previous):
        self.songs_path = path
        self.content = self.read()
        self.words = words

        if previous is None:
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
                song['song_id'] = parts[1]
                song['artist'] = parts[2]
                song['title'] = parts[3].strip('\n')

                songs.append(song)

        return songs

    def has_next(self):
        #return len(self.content) > 0

        # Do we need a condition? We just generate random names forever
        return True

    def next(self):
        if self.index < len(self.content):
            # Send out names from the list of known songs
            song = self.content[self.index]
            self.index += 1
            return song
        else:
            # Out of known songs, try generating names 
            return self.get_random_name()

    def get_random_name(self):
        name = ""
        for i in range(0, randint(1,3)):
            index = randint(0, len(self.words)-1)
            name += self.words[index] + " "

        return name

