from plugin import Plugin
import discord
import logging
import os
import pafy

class Trollolo(Plugin):

    async def initialize(self, bot):
        self.tag = 'troll'
        self.shortTag = 't'
        self.player = None

        self.commands.append('<rickroll><*>(username)<Rick Rolls the person by sending them the video privately>')
        self.commands.append('<nevergonna><0><Never gonna give you up! Never gonna let you down! Never gonna run around and desert you!>')
        self.commands.append('<trololo><0><Saruman has never sounded more beautiful>')
        self.commands.append('<isengard><0><They are taking the hobbits to isengardgardgardgagagagard>')
        self.commands.append('<heyeayea><0><And I said heyeayeayeayea! heyeayea! I said hey! What\'s going on?>')

        if not os.path.exists('troll'):
            os.makedirs('troll')

    async def _rickroll_(self, server, channel, author, username):
        person = discord.utils.get(server.members, name=username)

        if person == None:
            self.logger.debug('There is no user with this name.')
            await self.bot.send_message(channel, 'There is no user with this name.')
        else:
            self.logger.debug('Rick Rolling %s', person)
            await self.bot.send_message(person, 'https://www.youtube.com/watch?v=dQw4w9WgXcQ')

    async def playTroll(self, server, channel, url, filename):
        if self.bot.is_voice_connected(server):
            if not os.path.isfile('troll/' + filename + '.mp3'):
                self.dl_song(url, filename)

            if not self.is_playing():
                voiceChannel = self.bot.voice_client_in(server)
                self.player = voiceChannel.create_ffmpeg_player('troll/'+ filename + '.mp3') 
                self.player.start()
                return

        await self.bot.send_message(channel, url) 

    async def _nevergonna_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=dQw4w9WgXcQ'
        await self.playTroll(server, channel, url, 'nevergonna')

    async def _trololo_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=KaqC5FnvAEc'
        await self.playTroll(server, channel, url, 'trololo')

    async def _isengard_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=uE-1RPDqJAY'
        await self.playTroll(server, channel, url, 'isengard')

    async def _heyeayea_(self, server, channel, author):
        url = 'https://www.youtube.com/watch?v=ZZ5LpwO-An4'
        await self.playTroll(server, channel, url, 'heyeayea')

    def dl_song(self, url, name):
        video = pafy.new(url)
        audio = video.audiostreams
        songFile = audio[0].download(filepath="troll/" + name + ".mp3")

    def is_playing(self):
        return self.player is not None and self.player.is_playing()

    async def shutdown(self):
        self.player = None