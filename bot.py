from logging42 import logger
import nextcord
from nextcord.ext import commands

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

bot = commands.Bot()

# Load things from cfg
bot_token = cfg["bot token"]
message = cfg["message"]

# Print to log when successfully logged in
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')

# Command
@bot.slash_command(description='Say "F*ck you! to someone')
async def cogs(interaction: nextcord.Interaction, user: nextcord.Member):
    logger.debug(f'Saying f*ck you to {user.name} ({user.id}).')
    channel = bot.get_channel(interaction.channel_id)
    await interaction.send(f'Saying "{message}" to {user.mention}...', ephemeral=True)
    send_message = message.replace('[[mention]]', user.mention)
    channel.send(send_message)

# Run the Bot
bot.run(bot_token)
