import discord
from discord.ext import commands
from discord_slash import SlashCommand

with open("secret/bot_token.txt", "r") as token_file:
    TOKEN = token_file.read()

intents = discord.Intents().all()
bot = commands.Bot(command_prefix="d!", intents=intents)
slash = SlashCommand(bot, sync_commands=True)


async def dm(user: discord.User, message=None):
    message = message or "This message is sent via DM."
    try:
        await user.send(message)
        return True
    except discord.errors.HTTPException:
        print("Failed to send a DM to " + user.name + ". They likely do not have their DMs open to this bot.")
        return False


@bot.event
async def on_ready():
    print('Logged in as')
    print(str(bot.user.name) + " (" + str(bot.user.id) + ")")
    print('Servers connected to:')
    for guild in bot.guilds:
        print(str(guild.name) + " (" + str(guild.id) + ")")
    print('------')
    await dm(bot.get_user(83327063448092672), "DraftBot is now online.")


bot.run(TOKEN)
