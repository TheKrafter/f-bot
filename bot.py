from logging42 import logger
import nextcord
from nextcord.ext import commands
import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.FullLoader)

bot = commands.Bot()

# Load things from cfg
bot_token = cfg['bot token']
message = cfg['message']

# Check if moderation is enabled
def mod_enabled(guild_id):
    enabled = False
    with open("config.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    try:
        enabled = config['moderation'][guild_id]['enabled']
    except BaseException as ex:
        logger.warning(f'Tried to check if moderation is enabled, but failed! Error code: {ex}')
    return enabled

## These functions load values live from yaml
# Check what channel to put mod logs in
def mod_channel(guild_id):
    channel = 0
    with open("config.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    try:
        channel = config['moderation'][guild_id]['channel']
    except BaseException as ex:
        logger.warning(f'Tried to check where to send logs, but failed! Error code: {ex}')
    return channel
# Print to log when successfully logged in
@bot.event
async def on_ready():
    logger.info(f'Logged in as {bot.user}')
# Add yaml entry on guild join
@bot.event
async def on_guild_join(guild):
    logger.info(f'Joined a new guild! Name: {guild.name}, ID: {guild.id}')
    with open("config.yml", "r") as ymlfile:
        config = yaml.load(ymlfile, Loader=yaml.FullLoader)
    config['moderation'][guild.id]['enabled'] = False
    config['moderation'][guild.id]['channel'] = 0
    with open("config.yml", "w") as ymlfile:
        yaml.dump(config, ymlfile)
    logger.info(f'Added yml entry for guild {guild.name} (ID: {guild.id})')

# Command
@bot.slash_command(description='Say "F*ck you! to someone (anonymously, except mods may have loggin enabled)')
async def fu(interaction: nextcord.Interaction, user: nextcord.Member):
    logger.debug(f'Saying f*ck you to {user.name} ({user.id}).')
    channel = bot.get_channel(interaction.channel)
    if mod_enabled(interaction.guild_id):
        log_chan_id = mod_channel(interaction.guild_id)
        log_chan = bot.get_channel(log_chan_id)
        log_chan.send(f'User {interaction.user.mention} (ID: {interaction.user.id}) used the `/fu` command on {user.mention} (ID: {user.id}).')
        append = f'\n||*These commands are logged in this server.*||'
    else:
        append = f'\n||*These commands are **not** logged in this server.*||'
    await interaction.send(f'Saying "{message}" to {user.mention}...{append}', ephemeral=True)
    send_message = message.replace('[[mention]]', user.mention)
    channel.send(send_message)

# Mod config
@bot.slash_command(description='Whether to log uses of `/fu`, and where to put the log')
async def mod(interaction: nextcord.Interaction, enabled: bool, channel: nextcord.TextChannel):
    if interaction.user.guild_permissions.administrator:
        if enabled:
            with open("config.yml", "r") as ymlfile:
                config = yaml.load(ymlfile, Loader=yaml.FullLoader)
            config['moderation'][interaction.guild_id]['enabled'] = True
            config['moderation'][interaction.guild_id]['channel'] = channel.id
            with open("config.yml", "w") as ymlfile:
                yaml.dump(config, ymlfile)
            await interaction.send(f'Moderation logs are now **Enabled**, in {channel.mention}!')
        else:
            with open("config.yml", "r") as ymlfile:
                config = yaml.load(ymlfile, Loader=yaml.FullLoader)
            config['moderation'][interaction.guild_id]['enabled'] = False
            config['moderation'][interaction.guild_id]['channel'] = 0
            with open("config.yml", "w") as ymlfile:
                yaml.dump(config, ymlfile)
            await interaction.send(f'Moderation logs are now **Disabled**!')

# Run the Bot
bot.run(bot_token)
