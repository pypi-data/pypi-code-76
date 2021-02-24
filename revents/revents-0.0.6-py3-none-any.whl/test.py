import hikari
import uvloop
import asyncio
import lightbulb
from revents import EventClient

cache_settings = hikari.CacheSettings(
    invites=False,
    voice_states=False,
    messages=False
)

bot_settings = {
    "token": "Nzg1MTM1MjE3NTkyNTAwMjQ0.X8zcJg.8wK8zTktOZN4N95pQlS7VHm_Nto",
    "prefix": "milk.",
    "ignore_bots": True,
    "cache_settings": cache_settings,
    "intents": hikari.Intents.GUILD_MEMBERS
            | hikari.Intents.GUILD_MESSAGES
            | hikari.Intents.ALL_MESSAGE_REACTIONS
            | hikari.Intents.GUILDS
            | hikari.Intents.DM_MESSAGES
            | hikari.Intents.GUILD_EMOJIS
}

reddit_settings = {
    "client_id": "DeqFgJm-W3WjLw",
    "client_secret": "c30D8U1kGMYe_8tqhPKU2_AoswcWNA",
    "user_agent": "macOS:discord_feeds:v1.0 by /u/YodaSwitch"
}

bot = lightbulb.Bot(**bot_settings)
client = EventClient(**reddit_settings)

async def on_submission(submission):
    channel = bot.cache.get_guild_channel(785135959246110723)
    embed = hikari.Embed(title=f"{submission.title} ({submission.subreddit_name_prefixed})", url=submission.shortlink, description=submission.selftext)
    await submission.author.load()
    embed.set_footer(text=f"u/{submission.author}", icon=submission.author.icon_img)
    await channel.send(embed=embed)

@bot.command()
async def start(ctx):
    client.subscribe(on_submission, ["testingground4bots"])

@bot.command()
async def stop(ctx):
    client.unsubscribe(on_submission, ["testingground4bots"])

async def test(_):
    pass

client.subscribe(test, ["Python"])
client.run(run_forever=False)
bot.run()