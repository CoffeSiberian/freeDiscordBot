import random

class Queue:

    def __init__(self):
        self._queue = []
        self.position = 0

    @property
    def isEmpty(self):
        return not self._queue

    @property
    def currentTrack(self):
        if not self._queue:
            return False
        return self._queue[self.position]

    @property
    def upcoming(self):
        if not self._queue:
            return False
        return self._queue[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            return False
        return self._queue[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args):
        self._queue.extend(args)

    def setNextTrack(self):
        ''' 
        We set the next song, but if it does not exist. returns False
        '''
        if not self._queue:
            return False
        self.position += 1
        try:
            elemen = self._queue[self.position]
            return elemen
        except IndexError:
            self.empty()
            return False

    def shuffle(self):
        if not self._queue:
            return False
        upcoming = self.upcoming
        random.shuffle(upcoming)
        self._queue = self._queue[:self.position + 1]
        self._queue.extend(upcoming)

    def empty(self):
        self._queue.clear()
        self.position = 0