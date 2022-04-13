from nextcord.ext import commands

class DefaultCommands(commands.Cog, name='Default Commands'):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx, *args):
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

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