from interactions import *
from settings import *
import os
import keep_alive

cogs: list = [
    "Functions.Bugtracker.bug", "Functions.Bugtracker.bugmod",
    "Functions.Bugtracker.bugdel", "Functions.Bugtracker.bugclear",
    "Functions.Suggestions.suggest", "Functions.Suggestions.suggestmod",
    "Functions.Suggestions.suggestdel", "Functions.Suggestions.suggestclear",
    "Functions.Feedback.feedback", "Functions.Mod.reactionroles",
    "Functions.Mod.release", "Functions.Mod.clear", "Functions.Mod.clearall"
]

try:
    client = Client(token=os.getenv('TOKEN'))
except:
    os.system('kill 1')


@client.event
async def on_ready():
    print("Bot is ready!")
    await client.change_presence(
        ClientPresence(status=StatusType.ONLINE,
                       activities=[
                           PresenceActivity(name=BotStatus,
                                            type=PresenceActivityType.GAME,
                                            created_at=0)
                       ],
                       afk=False))


for cog in cogs:
    try:
        print(f"Loading cog {cog}")
        client.load(cog)
        print(f"Loaded cog {cog}")
    except Exception as e:
        exc = "{}: {}".format(type(e).__name__, e)
        print("Failed to load cog {}\n{}".format(cog, exc))

keep_alive.keep_alive()

try:
    client.start()
except:
    os.system('kill 1')
