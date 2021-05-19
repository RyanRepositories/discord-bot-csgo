# Made in 2021 by Ryan C.

# discord.py library
import discord
from discord.ext import commands

# Other files
import processes

# Command prefix and removes default help command
client = commands.Bot(command_prefix = "$", help_command=None)


@client.event
# Proves the bot is ready to be used upon running and fetches APIs
async def on_ready():
    processes.api_grabber()
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game('Searching Item Prices'))
    print("Bot is ready.")


@client.event
# If a command has been mistyped, send error message
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        embed = processes.error_message()
        await ctx.send(embed=embed)


@client.command()
# Help command
async def help(ctx, command=None):
    embed = processes.custom_help_output(command)
    await ctx.send(embed=embed)


@client.command()
# Displays prices, % increase, type of investment
async def price(ctx, skin_name=None, conversion_rate=None):
    embed = processes.price_output(skin_name, conversion_rate)
    await ctx.send(embed=embed)


if __name__ == "__main__":
    # Connects with Discord API for the bot to work
    token = "token"
    client.run(token)

    on_ready()
