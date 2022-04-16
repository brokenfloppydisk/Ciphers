from nextcord.ext import commands
from bot import cipher_bot

from ciphers.aristocrat_io import AristocratIO

class DefaultCommands(commands.Cog, name='Default Commands'):
    def __init__(self, bot: cipher_bot):
        self.bot = bot

    @commands.command()
    async def test(self, ctx: commands.Context, *args):
        await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

    @commands.group()
    async def cipher(self, ctx: commands.Context, args):
        """ Start solving a cipher
        """
        if ctx.invoked_subcommand is None or ctx.invoked_subcommand not in self.cipher.walk_commands():
            ctx.send(f"Unknown subcommand. Please enter {cipher_bot.get_subcommands(self.cipher.command)}")

        @commands.group()
        async def aristocrat(ctx: commands.Context):
            if ctx.invoked_subcommand is None:
                await ctx.send("Unknown aristocrat command. Please use generate, practice, or solve.")

            @aristocrat.command()
            async def generate(ctx: commands.Context):
                AristocratIO.generate_user_cipher()
            
            @aristocrat.command()
            async def practice(ctx: commands.Context):
                AristocratIO.practice_cipher()
            
            @aristocrat.command()
            async def solve(ctx: commands.Context, *args: str):
                if args is not None and args[0].lower() == "unknown":
                    AristocratIO.solve_unknown_cipher()
                else:
                    AristocratIO.solve_cipher()

    @commands.command()
    async def prefix(self, ctx: commands.Context, args):
        await ctx.channel.send(f"Prefix changed to `{str(args)}`!")
        self.command_prefix = str(args)