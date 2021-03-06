from functions.dirt import getConf
from bot.nocogs.music.spotify_url_validatio import idAndType
from bot.nocogs.music.validations import validaciones

config = getConf()

class MusicaSP:

    def __init__(self, bot, playSound, yt_instance, sp_instance):
        self.voldef = config['volumen']
        self.prefix = config['prefix']
        self.bot = bot
        self.pmusic = playSound
        self.validacion = validaciones(bot)
        self.apiyt = yt_instance
        self.apisp = sp_instance
    
    async def valid(self, ctx, url):
        valid = idAndType(url)
        if valid != False:
            if valid[0] == 'track':
                return await self.spPlayTrack(ctx, valid[1])
            elif valid[0] == 'playlist':
                return await self.spPlayPlayList(ctx, valid[1])
            return False
        return False

    async def spPlayTrack(self, ctx, id):
        if await self.validacion.isPossiblePlay(ctx):
            track = self.apisp.getTrack(id)
            if track[1] == 200:
                yplay = self.apiyt.search(track[0])
                await self.pmusic.playSound(ctx, yplay["entries"][0]["url"], names=track[0], img=track[2])
    
    async def spPlayPlayList(self, ctx, id):
        '''
        if it is found, it send a list with the names of the songs
        '''
        if await self.validacion.isPossiblePlay(ctx):
            track = self.apisp.getTracksPlaylist(id)
            if track[1] == 200:
                await self.pmusic.playSound(ctx, track[0], names=track[0], img=track[3])