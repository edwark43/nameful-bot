import discord, os, json, sys
sys.path.append("..")
import utils
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

class Member_List(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if os.getenv("SETUP") == "True":
            self.member_count_vc_task.start()
            self.member_list_channel_task.start()
    
    member = discord.SlashCommandGroup("member", "Interact with Member Data")

    @member.command(name="add", description="Add a Member to the Website Member List")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def addMember(
            self,
            ctx,
            username: discord.Option(str)
            ):
        codes = []
        parts = []

        for part in utils.split_username(username):
            try:
                if username[0] == "&":
                    int(part[0])
                else:
                    int("")
            except:
                codes.append("&f")
                parts.append(part)
            else:
                codes.append(f"&{part[0]}")
                parts.append(part[1:])

        if len(codes) == len(parts):
            data["memberList"]["members"].append({'colorCodes':codes,'username':parts})
        else:
            data["memberList"]["members"].append({'colorCodes':[],'username':parts})

        os.remove(os.getenv("JSON"))

        with open(os.getenv("JSON"), "w") as f:
            json.dump(data, f, indent=2)

        await ctx.respond(f"Added {username} to the member list.", ephemeral="True")

    @member.command(name="remove", description="Remove a Member from the Website Member List")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def removeMember(
            self,
            ctx,
            number: discord.Option(int, "Enter a number", min_value=1, max_value=len(data["memberList"]["members"]))
            ):
        try:
            data["memberList"]["members"].pop(number)
            os.remove(os.getenv("JSON"))

        except Exception as e:
            await ctx.respond(f"Error: {e}", ephemeral="True")
        else:
            with open(os.getenv("JSON"), "w") as f:
                json.dump(data, f, indent=2)

            await ctx.respond(f"Added {username} to the member list.", ephemeral="True")

    @tasks.loop(seconds=600)
    async def member_count_vc_task(self):
        channel = await self.bot.fetch_channel(int(os.getenv("MEMBER_COUNT_CHANNEL_ID")))

        await channel.edit(name=f"Town Member Count: {str(len(data['memberList']['members']))}")

    @tasks.loop(seconds=600)
    async def member_list_channel_task(self):
        load_dotenv(dotenv_path,override=True)
        channel = await self.bot.fetch_channel(int(os.getenv("MEMBER_LIST_CHANNEL_ID")))

        if int(os.getenv("SENT_MEMBERS")) < len(data["memberList"]["members"]):
            for i,member in enumerate(data["memberList"]["members"]):
                if i > int(os.getenv("SENT_MEMBERS")) - 1:
                    await channel.send(discord.utils.escape_markdown(utils.get_member(i + 1)))
                    set_key(dotenv_path, "SENT_MEMBERS", str(int(os.getenv("SENT_MEMBERS")) + 1))
                    load_dotenv(dotenv_path,override=True)

def setup(bot):
    bot.add_cog(Member_List(bot))
