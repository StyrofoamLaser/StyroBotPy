from plugin import Plugin
import discord
import styrobot
import random
import logging
import inspect
import commands

class Test(Plugin):

    async def initialize(self, bot):
        self.channelName = 'quotes'
        self.tag = 'test'
        self.shortTag = 'q'

        self.logger.debug('This Bot is part of %s servers!', str(len(self.bot.servers)))

        for server in self.bot.servers:
            settings = await self.bot.getSettingsForTag(server, self.tag)

            if 'channame' in settings:
                self.channelName = settings['channame']
            else:
                await self.bot.modifySetting(server, self.tag, 'channame', self.channelName)

        self.channel = discord.utils.get(server.channels, name=self.channelName, type=discord.ChannelType.text)

        if self.channel == None:
            self.logger.debug('No quotes channel found, creating channel')
            self.channel = await self.bot.create_channel(server, self.channelName)

    @styrobot.plugincommand('Overload test!', name='overload')
    async def _overload_(self, server, channel, author, **kwargs):
        await self.bot.send_message(channel, 'Overload Master')

    @styrobot.plugincommand('Overload test 1!', name='overload')
    async def _overload1_(self, server, channel, author, test1, **kwargs):
        await self.bot.send_message(channel, 'Overload 1: ' + test1)

    @styrobot.plugincommand('Overload test 2!', name='overload')
    async def _overload2_(self, server, channel, author, test1, test2, **kwargs):
        await self.bot.send_message(channel, 'Overload 2: ' + test1 + ' & ' + test2)

    @styrobot.plugincommand('Say a random quote from the quotes channel', name='quote')
    async def _quote_(self, server, channel, author, **kwargs):
        #print('Description:', Plugin.commandMetadata['Test._quote_']['_description'])
        print('Server: {}  Channel: {}  Author: {}'.format(server, channel, author))
        quotes = []
        async for message in self.bot.logs_from(self.channel, limit=1000000):
            quotes.append(message)

        if len(quotes) == 0:
            self.logger.debug('[quote]: There are no quotes in the %s channel!', self.channelName)
            await self.bot.send_message(channel, 'There are no quotes in the ' + self.channelName + ' channel!')
            return

        randQuote = quotes[random.randint(0, len(quotes) - 1)]

        self.logger.debug('[quote]: %s', randQuote.content)
        await self.bot.send_message(channel, randQuote.content)

    @styrobot.plugincommand('Says which channel is being used for quotes', name='channel')
    async def _channel_(self, server, channel, author):
        self.logger.debug('[channel]: The current quote channel is: %s', self.channelName)
        await self.bot.send_message(channel, 'The current quote channel is: ' + self.channelName)

    @styrobot.plugincommand('Changes the channel to use for quotes to the channel called <name>', name='setchannel')
    async def _setchannel_(self, server, channel, author, channame):
        self.logger.debug('[setchannel]: Finding channel with name [%s]', channame)
        newChan = discord.utils.get(server.channels, name=channame, type=discord.ChannelType.text)

        if newChan != None:
            self.channel = newChan 
            self.channelName = channame

            await self.bot.modifySetting(server, self.tag, 'channame', channame)

            self.logger.debug('[setchannel]: Quotes will now be taken from channel: %s', channame)
            await self.bot.send_message(channel, 'Quotes will now be taken from channel: ' + channame)

        else:
            self.logger.debug('[setchannel]: There is no channel with that name.')
            await self.bot.send_message(channel, 'There is no channel with that name.')

    @styrobot.plugincommand('Adds the text as a quote', name='add', parserType=commands.ParamParserType.ALL)
    async def _add_(self, server, channel, author, text):
        print('[add]: ', text)

    @styrobot.plugincommand('Creates a quote', name='create', parserType=commands.ParamParserType.CUSTOM, parser=lambda args: args.split('-'))
    async def _create_(self, server, channel, author, quote, quoter):
        print('[create]: ', quote, ' - ', quoter)
        print('Server: {}  Channel: {}  Author: {}  Quote: {}  Quoter: {}'.format(server, channel, author, quote, quoter))

    @styrobot.plugincommand('Blah blah blah', name='blah')
    async def _blah_(self, beep, boop, bop, **kwargs):
        print('Beep:', beep, 'Boop:', boop, 'Bop:', bop)
        print('Server: {}  Channel: {}  Author: {}'.format(kwargs['server'], kwargs['channel'], kwargs['author']))
