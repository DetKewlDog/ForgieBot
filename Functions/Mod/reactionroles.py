from interactions import *
from settings import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="rrsetup", description="Setup Reaction Roles", default_member_permissions=Permissions.ADMINISTRATOR,
        options=[Option(name="channel", description="The destination channel", type=OptionType.CHANNEL, required=True)])
    async def _rrsetup(self, ctx: CommandContext, channel):
        msg = 'Click on the <:forgeapprove:980531953801494598> **Subscriber** button to get notified when an announcement is posted\nClick on the <:forgethreaten:980531953667309608> **Spoilers** button to get notified when a spoiler/teaser is posted\nClick on any of the buttons again to disable notifications'

        btn_subscriber = Button(
            style=ButtonStyle.PRIMARY,
            label="Subscriber",
            custom_id="btn_subscriber"
        )

        btn_spoilers = Button(
            style=ButtonStyle.PRIMARY,
            label="Spoilers",
            custom_id="btn_spoilers"
        )

        btn_subscriber.emoji = await ctx.guild.get_emoji(934186475736678480)
        btn_spoilers.emoji = await ctx.guild.get_emoji(934181022059364352)
        channel = Channel(id=channel.id, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)

        await channel.send(msg, components=[btn_subscriber, btn_spoilers])
        await ctx.send('Created Roles message!', ephemeral=True)

    async def reaction_role(self, ctx, role_id):
        usr = ctx.author
        if role_id in usr.roles:
            await usr.remove_role(role_id, ctx.guild_id)
            await ctx.send(f"You no longer have the <@&{role_id}> role!", ephemeral=True)
        else:
            await usr.add_role(role_id, ctx.guild_id)
            await ctx.send(f"You now have the <@&{role_id}> role!", ephemeral=True)

    @extension_component("btn_subscriber")
    async def btn_subscriber_resp(self, ctx):
        await self.reaction_role(ctx, SUBSCRIBER_ROLE_ID)

    @extension_component("btn_spoilers")
    async def btn_spoilers_resp(self, ctx):
        await self.reaction_role(ctx, SPOILERS_ROLE_ID)

def setup(client):
    Ext(client)