from interactions import *
from settings import *
from requests import get
from json import loads
from io import StringIO
from interactions.ext.files import command_send
import re
import os


class Ext(Extension):

    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="release",
                       description="Announce release",
                       default_member_permissions=Permissions.ADMINISTRATOR,
                       options=[
                           Option(name="channel",
                                  description="The destination channel",
                                  type=OptionType.CHANNEL,
                                  required=True),
                           Option(name="content",
                                  description="The message content",
                                  type=OptionType.ATTACHMENT,
                                  required=True),
                           Option(name="links",
                                  description="The download links",
                                  type=OptionType.ATTACHMENT,
                                  required=True)
                       ])
    async def _release(self, ctx: CommandContext, channel, content, links):

        msg = get(content.url).text
        platforms = loads(get(links.url).text)
        print(platforms)

        btns = []

        for platform in platforms:
            btns.append(
                Button(style=5, label=platform, url=platforms[platform]))

        channel = Channel(id=channel.id,
                          type=ChannelType.GUILD_TEXT,
                          guild_id=ctx.guild_id,
                          _client=self.client._http)

        await channel.send(msg, components=btns)
        await ctx.send('Created Release message!', ephemeral=True)


def setup(client):
    Ext(client)
