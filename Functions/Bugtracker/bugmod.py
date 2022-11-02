from interactions import *
from settings import *
from bugreport import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="bugmod",
        description="Use this command to modify a bug",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[
            Option(name='closed', description="Close a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='inprogress', description="In Progress a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='open', description="Open a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='postponed', description="Postpone a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='resolved', description="Resolve a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='wontfix', description="Don't fix a bug", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
        ]
    )

    async def _bugmod(self, ctx: CommandContext, sub_command: str, id):
        id = id.zfill(3)
        msg_id = 0
        lines = []

        found = False
        with open(BUG_REPORTS_DIR, "r") as file:
            for line in file:
                if ' ' + id + ' ' in line:
                    msg_, id, st = line.split(' ')
                    lines.append(str(BugReport(msg_, id, sub_command.lower())) + '\n')
                    msg_id = msg_
                    found = True
                else:
                    lines.append(line)

        if not found:
            await ctx.send('Couldn\'t find bug with given ID!', ephemeral=True)
            return
        with open(BUG_REPORTS_DIR, "w") as file:
            file.writelines(lines)

        msg = await Message.get_from_url(msg_id, client=self.client._http)

        embed2 = msg.embeds[0]
        embed2.color = BUG_STATUSES[sub_command]
        if sub_command == 'inprogress':
            sub_command = 'in progress'
        embed2.title = f'Bug #{id} ({sub_command.upper()})'
        await msg.edit(embeds=[embed2])
        await ctx.send('Updated bug!', ephemeral=True)

def setup(client):
    Ext(client)