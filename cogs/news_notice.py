import discord, sys, os, json, requests
sys.path.append("..")
import utils
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()
path = "/home/lucas/website/newnameful.com/assets/json/data/media"
relativePath = "/assets/json/data/media"

class NewsNotice(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.news_notice_channel_task.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == int(os.getenv("NEWS_NOTICE_CHANNEL_ID")):
            if len(message.attachments) == 0:
                await message.delete()

    @tasks.loop(seconds=600)
    async def news_notice_channel_task(self):
        load_dotenv(dotenv_path,override=True)
        channel = await self.bot.fetch_channel(int(os.getenv("NEWS_NOTICE_CHANNEL_ID")))

        newsCount = 0
        async for message in channel.history():
            if len(message.attachments) >= 0:
                newsCount += 1

        if int(os.getenv("SENT_NEWS")) < newsCount:
            i = 0
            async for message in channel.history(limit=None, oldest_first=True):
                i += 1
                if len(message.attachments) > 0:
                    if i > int(os.getenv("SENT_NEWS")) - 1:
                        attachments = ""
                        for j,attachment in enumerate(message.attachments):
                            attachmentFileName = f"issue-{i}-{j}"
                            print(attachmentFileName)
                            with open(f"{path}/{attachmentFileName}.png",'wb') as f:
                                f.write(requests.get(message.attachments[j].url).content)
                            attachments += f"{{\"url\":\"{relativePath}/{attachmentFileName}.png\"}},"
                        avatarFileName = f"{message.author.name}"
                        if not os.path.isfile(f"{path}/{avatarFileName}.png"):
                            with open(f"{path}/{avatarFileName}.png",'wb') as f:
                                f.write(requests.get(message.author.display_avatar).content)
                        jsonObject=json.loads(f"{{\"timestamp\":\"{message.created_at}\",\"author\":{{\"nickname\":\"{message.author.display_name}\",\"avatarUrl\":\"{relativePath}/{avatarFileName}.png\"}},\"attachments\":[{attachments[:-1]}]}}")

                        data["newsNotice"]["messages"].append(jsonObject)

                        os.remove(os.getenv("JSON"))

                        with open(os.getenv("JSON"), "w") as f:
                            json.dump(data, f, indent=2)
                        set_key(dotenv_path, "SENT_NEWS", str(int(os.getenv("SENT_NEWS")) + 1))
                        load_dotenv(dotenv_path,override=True)

def setup(bot):
    bot.add_cog(NewsNotice(bot))
