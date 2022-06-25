class Queue:

    def __init__(self, guildId):
        self.guildId = guildId
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
        if type(args[0]) is list:
            return self._queue.extend(args[0])
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

    def back(self):
        if not self._queue:
            return False
        if self.position == 0:
            return False
        self.position -= 2
    
    def skip(self, pos):
        if not self._queue:
            return False
        if  pos > 0 and pos > self.position and pos < len(self._queue):
            self.position = pos-1
            return True
        return False

    def empty(self):
        self._queue.clear()
        self.position = 0