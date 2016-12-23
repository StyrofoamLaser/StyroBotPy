import abc
import logging
import inspect
from commands import CommandRegistry

class Plugin:
    __metaclass__ = abc.ABCMeta

    # Private initialize function
    # DO NOT OVERRIDE OR CALL EXPLICITELY
    async def _init(self, name, bot): 
        self.bot = bot
        self.tag = name
        self.shortTag = name[0]
        self.commands = []
        self.logger = logging.getLogger('styrobot.' + name)

        await self.initialize(bot)
        
        #self.parsedCommands = self._parseCommands()
        print('Plugin Class:', self.__class__.__name__)
        print('Commands:', self.parsedCommands)

    # Initializes the plugin
    # @param bot  A reference to the bot's instance
    @abc.abstractmethod
    async def initialize(self, bot): pass

    # Gets the list of commands and their descriptions that this plugin can do
    # Format: !<tag> <commandname> <parameters>  - <description>
    # example: !file save <url> <name>  - Saves the file at <url> to a local file named <name>
    # @return  An array of strings formatted like the example above
    def getCommands(self):
        commands = []

        for key, value in self.parsedCommands.items():
            str = '**!{} {} '.format(self.tag, key)
        
            if len(value[CommandRegistry.PARAM_NAMES]) != 0:
                for paramName in value[CommandRegistry.PARAM_NAMES]:
                    str += '<{}> '.format(paramName)

            str += '**  - {}'.format(value[CommandRegistry.DESCRIPTION])

            commands.append(str)

        return commands

    # Private helper function to parse the commands array and produce a dictionary
    # which contains all the information for each command
    def _parseCommands(self):
        commands = {}
        for com in self.commands:
            temp = com.split('<')
            temp2 = temp[2].split('>')
            name = temp[1][:-1]
            description = temp[3][:-1]
            numParams = temp2[0]
            paramNames = []
            if (len(temp2) > 1 and ((numParams != '*' and int(numParams) != 0) or numParams == '*')):
                paramNames = temp2[1][1:-1].split(',')

            commands[name] = {}
            commands[name][CommandRegistry.NUM_PARAMS] = numParams
            commands[name][CommandRegistry.PARAM_NAMES] = paramNames
            commands[name][CommandRegistry.DESCRIPTION] = description

        return commands

    # Checks if this plugin handles the command provided by the user 
    # @param tag      The tag which identifies the plugin (this could be their short tag)
    # @param command  The command the user wants to execute
    # @param args     The remaining text, which will be parsed into args for execution
    # @return         Returns False if it can't handle it. If it can, it returns the parsed args in an array
    def checkForCommand(self, tag, command, args): 
        if tag != self.tag and tag != self.shortTag:
            return False
    
        for key, value in self.parsedCommands.items():
            if key == command:
                temp = value[CommandRegistry.PARAM_PARSER](args)
                num = int(value[CommandRegistry.NUM_PARAMS])

                self.logger.debug('Command Found!')

                # Break out early if no params
                if num == 0:
                    return []

                # For some reason doing array[:0] will still slice elements so we need to check
                # for this edge case
                if len(temp)-num == 0:
                    self.logger.debug('Args: %s', temp)
                    return temp
                else:
                    self.logger.debug('Args: %s', temp[:len(temp)-num]) 
                    return temp[:len(temp)-num]

        return False

    # Executes the chat command 
    # @param channel     The discord channel this command was executed in
    # @param author      The user which executed this command
    # @param command     The command to execute
    # @param args        Any extra parameters that followed the command
    async def executeCommand(self, args, **kwargs):
        command = kwargs.pop('command')
        num = self.parsedCommands[command][CommandRegistry.NUM_PARAMS]
        paramNames = self.parsedCommands[command][CommandRegistry.PARAM_NAMES]
        funcName = self.parsedCommands[command][CommandRegistry.FUNCTION_NAME]

        if len(args) != len(paramNames):
            self.logger.error('The number of arguments (%s) and the number of parameter names (%s) does not match!', len(args), len(paramNames))

        for i, name in enumerate(paramNames):
            kwargs[name] = args[i]

        self.logger.debug('Executing command [%s] with arguments [%s]', command, str(args)[1:-1])
        await getattr(self, funcName)(**kwargs)

    # Whether or not this plugin wants to read messages completely
    # Override this if you want your plugin to read messages completely for something
    # @return  False if you don't want to read messages, True otherwise
    def isReadingMessages(self):
        return False

    # Allows the plugin to read the full message and do whatever they want with it
    # It is not recommend to handle commands in this function.
    # @param message  The message as given by discord. See discord documentation on the message class 
    async def readMessage(self, message): pass

    # An event that is called when the bot joins a voice channel. Override if you need
    # to handle something when this happens
    async def onJoinVoiceChannel(self): pass

    # An event that is called when the bot leaves a voice channel. Override if you need
    # to handle something when this happens
    async def onLeaveVoiceChannel(self): pass

    # Shutdowns the plugin
    async def shutdown(self): pass

