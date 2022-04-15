import asyncio
from tokenize import Double
import nextcord
from nextcord.ext import commands
from commands.default_commands import DefaultCommands

class cipher_bot(commands.Bot):
    ciphers_dict = {
        "aristocrat" : (lambda : ())
    }

    def __init__(self, command_prefix, help_command=None, description=None, self_bot=False) -> None:
        """ Initialize the bot. Calls bot.__init__()
        """
        commands.Bot.__init__(self, command_prefix=command_prefix, help_command=help_command, 
                              description=description, self_bot=self_bot)
        
        self.cipher_context: commands.Context = None

        self.most_recent_message: nextcord.Message = None
        self.new_content: bool = False

        self.add_cog(DefaultCommands(self))

    async def on_ready(self) -> None:
        """ Runs when the bot initializes.
        """
        print(f"{self.user.name} initialized")
        print(f"ID: {self.user.id}")
    
    async def fetch_message(self, author: nextcord.abc.User, check_rate: Double=0.5) -> nextcord.Message:
        """ Fetch the next message that has the same author.
        """
        while not self.new_content and self.most_recent_message.author == author:
            await asyncio.sleep(check_rate)
        self.new_content = False
        return self.most_recent_message

    async def fetch_message(self, condition, check_rate: Double=0.5) -> nextcord.Message:
        """ Fetch the next message that matches the condition
            condition should be a function (annotating this is not currently supported by Python)
        """
        while not self.new_content and condition():
            await asyncio.sleep(check_rate)
        self.new_content = False
        return self.most_recent_message

    async def on_message(self, message: nextcord.Message) -> None:
        """ Called every time a message is sent
        """
        # Set as the most recent message for fetch_message()
        self.new_content = True
        self.most_recent_message = message

        # Run all commands
        await self.process_commands(message)

bot = cipher_bot(command_prefix=["!"], description="Cipher Bot")

# Get bot token
with open("token.txt", "r") as t:
    token = t.read()
    bot.run(token.strip())