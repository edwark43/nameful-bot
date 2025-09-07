import discord, sys, os, json
sys.path.append("..")
import utils
from discord.ext import tasks, commands
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

class Constitution(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if os.getenv("SETUP") == "True":
            self.constitution_channel_task.start()

    amendment = discord.SlashCommandGroup("amendment", "Interact with Amendment Data")
    
    @amendment.command(name="add", description="Add an Amendment to the Constitution")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def addAmendment(
            self,
            ctx,
            section: discord.Option(int, "Enter a number", min_value=1, max_value=len(data["constitution"]["sections"])),
            content: discord.Option(str)
            ):

        data["constitution"]["sections"][section-1]["amendments"].append({'amendment':content})

        os.remove(os.getenv("JSON"))

        with open(os.getenv("JSON"), "w") as f:
            json.dump(data, f, indent=2)

        await ctx.respond(f"Added amendment to the constitution.", ephemeral="True")

    @tasks.loop(seconds=600)
    async def constitution_channel_task(self):
        load_dotenv(dotenv_path,override=True)
        channel = await self.bot.fetch_channel(int(os.getenv("CONSTITUTION_CHANNEL_ID")))

        amendmentCount = 0
        for section in data["constitution"]["sections"]:
            for amendment in section["amendments"]:
                amendmentCount += 1

        if int(os.getenv("SENT_AMENDMENTS")) < amendmentCount:
            async for message in channel.history():
                await message.delete()

            for section in data["constitution"]["sections"]:
                embed = discord.Embed(
                        title=section["title"],
                        description=section["preamble"],
                        color=utils.random_color()
                        )
                embed.set_author(name="Constitution")
                for j, amendment in enumerate(section["amendments"]):
                    embed.add_field(name=f"Amendment {str(j+1)}", value=amendment["amendment"])
                await channel.send(embed=embed)
            set_key(dotenv_path, "SENT_AMENDMENTS", str(amendmentCount))

def setup(bot):
    bot.add_cog(Constitution(bot))
