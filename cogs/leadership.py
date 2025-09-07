import discord, os, json, sys
sys.path.append("..")
import utils
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

class Leadership(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if os.getenv("SETUP") == "True":
            self.leadership_vc_task.start()
    
    leader = discord.SlashCommandGroup("leader", "Interact with Leader Data")

    @leader.command(name="edit", description="Edit a Ruler on the Website")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def editLeader(
            self,
            ctx,
            number: discord.Option(int, "Enter a number", min_value=1, max_value=len(data["leadership"]["leaders"])),
            username: discord.Option(str, "Enter a username")
            ):
        try:
            data["leadership"]["leaders"][number-1]["username"] = username
        except:
            await ctx.respond(f"Error: There is no leader {str(number)}.", ephemeral="True")
        else:
            os.remove(os.getenv("JSON"))

            with open(os.getenv("JSON"), "w") as f:
                json.dump(data, f, indent=2)

            await ctx.respond(f"Changed {data['leadership']['leaders'][number-1]['title']} to {username}.", ephemeral="True")

    @leader.command(name="add", description="Add a Leader to the Leader List")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def addLeader(
            self,
            ctx,
            title: discord.Option(str),
            username: discord.Option(str)
            ):
        try:
            data["leadership"]["leaders"].append({'title':title,'username':username})
        except:
            await ctx.respond("Error", ephemeral="True")
        else:
            os.remove(os.getenv("JSON"))

            with open(os.getenv("JSON"), "w") as f:
                json.dump(data, f, indent=2)

            await ctx.respond(f"Added {username} as {title}.", ephemeral="True")

    @tasks.loop(seconds=600)
    async def leadership_vc_task(self):
        channel1 = await self.bot.fetch_channel(int(os.getenv("RULER_CHANNEL_ID")))
        channel2 = await self.bot.fetch_channel(int(os.getenv("CO_RULER_CHANNEL_ID")))

        await channel1.edit(name=f"Ruler: {data['leadership']['leaders'][0]['username']}")
        await channel2.edit(name=f"Co-Ruler: {data['leadership']['leaders'][1]['username']}")

def setup(bot):
    bot.add_cog(Leadership(bot))
