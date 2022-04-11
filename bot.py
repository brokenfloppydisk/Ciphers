import nextcord
from nextcord.ext import commands


class cipher_bot(commands.Bot):

    ciphers_dict = {
        "aristocrat" : (lambda : ())
    }

    def __init__(self):
        self.command_prefix = "!"
        self.cipher_context: commands.Context = None

    @commands.command()
    async def cipher(self, ctx: commands.Context, args):
        """ Start solving a cipher
        """
        self.cipher_context = ctx

        if args in self.ciphers_dict:
            await self.ciphers_dict[args]()
    
    @commands.command()
    async def prefix(self, ctx: commands.Context, args):
        await ctx.channel.send(f"Prefix changed to `{str(args)}`!")
        self.command_prefix = str(args)

bot = cipher_bot(command_prefix=["c! "], description="Cipher Bot")

# Get bot token
with open("token.txt", "r") as t:
    token = t.read()
    bot.run(token.strip())