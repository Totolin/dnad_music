from Queue import Queue
from threading import Thread
from random import randrange

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


def worker_job(name, spotify, mongo):
	# This is what the worker (1 thread) will execute
	# Using the song's name, send a request to Spotify
	# result = spotify.get_song(name)
	print name
	print spotify

class ThreadPool:
    #Pool of threads consuming tasks from a queue
    def __init__(self, num_threads):
        self.tasks = Queue(num_threads)
        for _ in range(num_threads): Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        #Add a task to the queue
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        #Wait for completion of all the tasks in the queue
        self.tasks.join()

class Researcher:

    def __init__(self, generator, spotify, database):
    	self.generator = generator
    	self.spotify = spotify
    	self.database = database

    def create(self):
	    delays = [randrange(1, 10) for i in range(100)]
	    
	    from time import sleep
	    def wait_delay(d):
	        print 'sleeping for (%d)sec' % d
	        sleep(d)
	    
	    # 1) Init a Thread pool with the desired number of threads
	    pool = ThreadPool(20)
	    
	    for i, d in enumerate(delays):
	        # print the percentage of tasks placed in the queue
	        print '%.2f%c' % ((float(i)/float(len(delays)))*100.0,'%')
	        
	        # 2) Add the task to the queue
	        pool.add_task(wait_delay, 'asd', i)
	    
	    # 3) Wait for completion
	    pool.wait_completion()

