import discord
from discord.ext import commands

import ciphers.aristocrat as aristo
import ciphers.alphabet as alpha
import ciphers.quotes as quotes
from ciphers.alphabet import Alphabet

bot = commands.Bot(command_prefix=["c! "], description="Cipher Bot")

# Get bot token
with open("token.txt", "r") as t:
    token = t.read()
    bot.run(token.strip())