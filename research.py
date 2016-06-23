from Queue import Queue
from threading import Thread
from random import randrange
from time import sleep


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            func, args, kargs = self.tasks.get()
            try: func(*args, **kargs)
            except Exception, e: print e
            self.tasks.task_done()


def worker_job(song, spotify, mongo):
    # This is what the worker (1 thread) will execute
    # Using the song's name, send a request to Spotify
    sp_qr = song["artist"] + ' - ' + song["title"]
    result = spotify.get_song(sp_qr)

    # Error while calling API
    if result is None:
        print "[ERROR] Researching song: " + song["title"]
        return

    # Song not found
    if len(result) < 2:
        print "[ERROR] Song not found in Spotify: " + song["title"]
        return

    print 'Succesfully researched song: ' + song["artist"] + ' - ' + song["title"]

    # Insert received song into the database
    mongo.insert(result)


class ThreadPool:
    # Pool of threads consuming tasks from a queue
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        # Add a task to the queue
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        # Wait for completion of all the tasks in the queue
        self.tasks.join()


class Researcher:

    def __init__(self, generator, spotify, database):
        self.generator = generator
        self.spotify = spotify
        self.database = database

    def start(self):

        # Init a Thread pool with the desired number of threads
        pool = ThreadPool(20)
        
        while self.generator.has_next():
            # print the percentage of tasks placed in the queue
            #print '%.2f%c' % ((float(i)/float(len(delays)))*100.0,'%')

            pool.add_task(
                # Thread job
                worker_job,
                # Next song name
                self.generator.next(),
                # Spotify API Caller
                self.spotify,
                # MongoDB interface
                self.database
            )
        
        # Wait for completion
        pool.wait_completion()

