from interactions import *
from settings import *
from bugreport import *
from datetime import datetime
from validators import url

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="bug", description="Use this command to report a bug")
    async def _bug(self, ctx: CommandContext):
      if 877157510539247657 in ctx.author.roles:
        modal = Modal(
            title="Bug Report",
            custom_id="bug_report",
            components=[
                TextInput(style=TextStyleType.SHORT, label="Describe the bug:", custom_id="title"),
                TextInput(style=TextStyleType.SHORT, label="Enter build version:", custom_id="version"),
                TextInput(style=TextStyleType.SHORT, label="Enter build platform:", custom_id="platform"),
                TextInput(style=TextStyleType.PARAGRAPH, label="Describe the bug + repo steps:", custom_id="description"),
                TextInput(style=TextStyleType.SHORT, label="Enter image/video link (optional):", custom_id="link", required=False)
            ],
        )

        await ctx.popup(modal)

    @extension_modal("bug_report")
    async def bug_report_resp(self, ctx,  title, version, platform, description, link = None):
        report_date = datetime.now().strftime("%d/%m/%Y, %H:%M:%S")

        bug_id = f"{(len(open(BUG_REPORTS_DIR).readlines()) + 1):03}"
        report = Embed(
            title='Bug #' + bug_id + ' (OPEN)',
            color=COLOR_OPEN,
            fields=[
                EmbedField(name='Bug:', value=title, inline=False),
                EmbedField(name='Version:', value=version, inline=False),
                EmbedField(name='Platform:', value=platform, inline=False),
                EmbedField(name='Issuer:', value=ctx.author.mention, inline=False),
                EmbedField(name='Issued On:', value=report_date, inline=False),
                EmbedField(name='Description:', value=description, inline=False)
            ]
        )
        if link:
            if url(link):
                report.set_image(url=link)
            else:
                report.add_field('Image could not be loaded!', 'The provided link could not be opened!')
        report_channel = Channel(id=REPORT_CHANNEL_ID, type=ChannelType.GUILD_TEXT, guild_id=ctx.guild_id, _client=self.client._http)
        report_msg = await report_channel.send(embeds=[report])
        report_id = report_msg.url
        with open(BUG_REPORTS_DIR, "a") as f:
            bug = BugReport(report_id, bug_id, "open")
            f.write(str(bug) + '\n')

        await ctx.send(f"Successfully reported bug!\n[Click here to view the report]({report_id})", ephemeral=True)

def setup(client):
    Ext(client)