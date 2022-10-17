from interactions import *
from settings import *
from suggestion import *
from datetime import datetime
from validators import url

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="suggest", description="Use this command to suggest an idea")
    async def _suggest(self, ctx: CommandContext):
      if 877157510539247657 in ctx.author.roles:
        modal = Modal(
            title="Suggestion",
            custom_id="suggestion",
            components=[
                TextInput(style=TextStyleType.SHORT, label="Give the idea a title:", custom_id="title"),
                TextInput(style=TextStyleType.PARAGRAPH, label="Describe the idea:", custom_id="description"),
                TextInput(style=TextStyleType.SHORT, label="Enter image/video link (optional):", custom_id="link", required=False),
            ]
        )

        await ctx.popup(modal)

    @extension_modal("suggestion")
    async def suggestion_resp(self, ctx, title, description, link = None):
        report_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        suggestion_id = f"{(len(open(SUGGESTIONS_DIR).readlines()) + 1):03}"
        report = Embed(
            title='Suggestion #' + suggestion_id,
            color=COLOR_SUGGESTION,
            fields=[
                EmbedField(name='Idea:', value=title, inline=False),
                EmbedField(name='Suggested by:', value=ctx.author.mention, inline=False),
                EmbedField(name='Suggested On:', value=report_date, inline=False),
                EmbedField(name='Description:', value=description, inline=False)
            ]
        )
        if link:
            if url(link):
                report.set_image(url=link)
            else:
                report.add_field('Image could not be loaded!', 'The provided link could not be opened!')
        suggest_channel = Channel(id=SUGGESTION_CHANNEL_ID, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)
        report_msg = await suggest_channel.send(embeds=[report])

        await report_msg.create_reaction('✅')
        await report_msg.create_reaction('❌')

        report_id = report_msg.url
        with open(SUGGESTIONS_DIR, "a") as f:
            bug = Suggestion(report_id, suggestion_id)
            f.write(str(bug) + '\n')

        await ctx.send(f"Successfully suggested idea!\n[Click here to view the report]({report_id})", ephemeral=True)

def setup(client):
    Ext(client)