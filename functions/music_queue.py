class Queue:

    def __init__(self, guildId):
        self.guildId = guildId
        self._queue = []
        self.nameMusic = []
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
        return self._queue[self.position + 1:], self.nameMusic[self.position + 1:]

    @property
    def history(self):
        if not self._queue:
            return False
        return self._queue[:self.position], self.nameMusic[:self.position]

    @property
    def length(self):
        return len(self._queue)

    def add(self, *args, names):
        if type(args[0]) is list:
            self._queue.extend(args[0])
            self.nameMusic.extend(names)
            return True
        self._queue.extend(args)
        self.nameMusic.extend([names])

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
    
    #only for test
    def test(self):
        print(self.history)
        print(self.upcoming)