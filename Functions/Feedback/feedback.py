from interactions import *
from settings import *
from datetime import datetime

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="feedback", description="Use this command to give us feedback!")
    async def _feedback(self, ctx: CommandContext):
      if 877157510539247657 in ctx.author.roles:
        modal = Modal(
            title="Feedback",
            custom_id="feedback",
            components=[
                TextInput(style=TextStyleType.SHORT, label="For how long did you play? (check main menu):", custom_id="playtime"),
                TextInput(style=TextStyleType.PARAGRAPH, label="What do you think of Forgescape?", custom_id="opinion"),
                TextInput(style=TextStyleType.PARAGRAPH, label="Did you enjoy playing Forgescape?", custom_id="enjoyment"),
                TextInput(style=TextStyleType.PARAGRAPH, label="Would you recommend Forgescape to others?", custom_id="recommendation"),
                TextInput(style=TextStyleType.PARAGRAPH, label="What can be improved upon in Forgescape?", custom_id="improvement"),
            ]
        )

        await ctx.popup(modal)

    @extension_modal("feedback")
    async def feedback_resp(self, ctx, playtime, opinion, enjoyment, recommendation, improvement):
        report_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")
        report = Embed(
            title='Feedback Form',
            color=COLOR_OPEN,
            fields=[
                EmbedField(name='Sent by:', value=ctx.author.mention, inline=False),
                EmbedField(name='Sent On:', value=report_date, inline=False),
                EmbedField(name='For how long did you play?', value=playtime, inline=False),
                 EmbedField(name='What do you think of Forgescape?', value=opinion, inline=False),
                EmbedField(name='Did you enjoy playing Forgescape?', value=enjoyment, inline=False),
                EmbedField(name='Would you recommend Forgescape to others?', value=recommendation, inline=False),
                EmbedField(name='What can be improved upon in Forgescape?', value=improvement, inline=False)
            ]
        )
        feedback_channel = Channel(id=FEEDBACK_CHANNEL_ID, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)
        await feedback_channel.send(embeds=[report])

        report.color = COLOR_CLOSED

        await ctx.send(f"Successfully suggested idea!\nWe recorded these answers:", embeds=[report], ephemeral=True)

def setup(client):
    Ext(client)