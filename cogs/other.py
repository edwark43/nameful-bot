import discord, sys, os
sys.path.append("..")
import utils
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

class Other(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(name="archive", description="Archive a Channel")
    @discord.commands.guild_only()
    @discord.commands.default_permissions(administrator=True)
    async def archive(
            self,
            ctx,
            channel: discord.Option(discord.SlashCommandOptionType.channel, "Choose a channel")
            ):
        category = discord.utils.get(ctx.guild.categories, id=int(os.getenv("ARCHIVED_CATEGORY_ID"))) 

        await channel.move(end=True, category=category, sync_permissions=True)
        await ctx.respond("Archived Channel Successfully", ephemeral=True)

    pingHunter = discord.SlashCommandGroup("ping-hunter", ":troll~1:")

    @pingHunter.command(name="on", description=":troll~1:")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def onPingHunter(self, ctx):
        ctx.respond("<:troll~1:1414011614256173107>", ephemeral=True)
        self.ping_hunter_task.start()

    @pingHunter.command(name="off", description="😞")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def offPingHunter(self, ctx):
        ctx.respond("😞", ephemeral=True)
        self.ping_hunter_task.stop()

    @tasks.loop(seconds=1)
    async def ping_hunter_task(self):
        channel = await self.bot.fetch_channel(int(os.getenv("PING_HUNTER_CHANNEL_ID")))

        await channel.send("<@1104370538706632735>")




def setup(bot):
    bot.add_cog(Other(bot))
