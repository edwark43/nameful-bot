import os, discord
from discord.ext import tasks, commands
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

bot = discord.Bot(intents=discord.Intents.all())

@bot.event
async def on_ready():
    print(f"{bot.user} has started.")

cogs_list = [
    "leadership",
    "election",
    "member_list",
    "constitution",
    "news_notice",
    "other"
]

for cog in cogs_list:
    bot.load_extension(f"cogs.{cog}")

bot.run(os.getenv("TOKEN"))
