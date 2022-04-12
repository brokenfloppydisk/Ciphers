import nextcord
from nextcord.ext import commands
from commands.default_commands import DefaultCommands

class cipher_bot(commands.Bot):
    ciphers_dict = {
        "aristocrat" : (lambda : ())
    }

    def __init__(self, command_prefix, help_command=None, description=None, self_bot=False):
        commands.Bot.__init__(self, command_prefix=command_prefix, help_command=help_command, description=description, self_bot=self_bot)
        self.cipher_context: commands.Context = None
        self.add_cog(DefaultCommands(self))

    async def on_ready(self):
        print(f"{self.user.name} initialized")
        print(f"ID: {self.user.id}")

bot = cipher_bot(command_prefix=["!"], description="Cipher Bot")

# Get bot token
with open("token.txt", "r") as t:
    token = t.read()
    bot.run(token.strip())