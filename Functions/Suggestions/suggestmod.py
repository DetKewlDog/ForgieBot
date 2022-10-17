from interactions import *
from settings import *
from suggestion import *

class Ext(Extension):
    def __init__(self, client: Client) -> None:
        self.client: Client = client

    @extension_command(name="suggestmod",
        description="Use this command to modify a suggestion",
        default_member_permissions=Permissions.ADMINISTRATOR,
        options=[
            Option(name='announced', description="Announce a suggestion", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)]),
            Option(name='rejected', description="Reject a suggestion", type=OptionType.SUB_COMMAND, options=[
                Option(name="id", description="The ID of the bug report", type=OptionType.STRING, required=True)])
        ]
    )

    async def _suggestmod(self, ctx: CommandContext, sub_command: str, id):
        id = id.zfill(3)
        msg_id = 0
        lines = []

        found = False
        with open(SUGGESTIONS_DIR, "r") as file:
            for line in file:
                if ' ' + id in line:
                    msg_, id = line.split(' ')
                    lines.append(str(Suggestion(msg_, id)) + '\n')
                    msg_id = msg_
                    found = True
                else:
                    lines.append(line)

        if not found:
            await ctx.send('Couldn\'t find suggestion with given ID!', ephemeral=True)
            return
        with open(SUGGESTIONS_DIR, "w") as file:
            file.writelines(lines)

        msg = await Message.get_from_url(msg_id, client=self.client._http)

        embed2 = msg.embeds[0]
        embed2.color = SUGGEST_STATUSES[sub_command]
        embed2.title = f'Suggestion #{id} ({sub_command.upper()})'
        await msg.edit(embeds=[embed2])
        await ctx.send('Updated suggestion!', ephemeral=True)

def setup(client):
    Ext(client)