import discord, sys, os, json
sys.path.append("..")
import utils
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

class NewsNotice(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if os.getenv("SETUP") == "True":
            self.news_notice_channel_task.start()

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id == int(os.getenv("NEWS_NOTICE_CHANNEL_ID")):
            if len(message.attachments) == 0:
                await message.delete()
            else:
                attachments = ""
                for i,attachment in enumerate(message.attachments):
                    attachments += f"{{\"url\":\"{message.attachments[i].url}\"}},"
                jsonObject=json.loads(f"{{\"timestamp\":\"{message.created_at}\",\"author\":{{\"nickname\":\"{message.author.display_name}\",\"color\":\"{message.author.color}\",\"avatarUrl\":\"{message.author.display_avatar}\"}},\"attachments\":[{attachments[:-1]}]}}")

                data["newsNotice"]["messages"].append(jsonObject)

                os.remove(os.getenv("JSON"))

                with open(os.getenv("JSON"), "w") as f:
                    json.dump(data, f, indent=2)

                set_key(dotenv_path, "SENT_NEWS", str(int(os.getenv("SENT_NEWS")) + 1))
                load_dotenv(dotenv_path,override=True)

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
                            attachments += f"{{\"url\":\"{message.attachments[j].url}\"}},"
                        jsonObject=json.loads(f"{{\"timestamp\":\"{message.created_at}\",\"author\":{{\"nickname\":\"{message.author.display_name}\",\"color\":\"{message.author.color}\",\"avatarUrl\":\"{message.author.display_avatar}\"}},\"attachments\":[{attachments[:-1]}]}}")

                        data["newsNotice"]["messages"].append(jsonObject)

                        os.remove(os.getenv("JSON"))

                        with open(os.getenv("JSON"), "w") as f:
                            json.dump(data, f, indent=2)
                        set_key(dotenv_path, "SENT_NEWS", str(int(os.getenv("SENT_NEWS")) + 1))
                        load_dotenv(dotenv_path,override=True)

def setup(bot):
    bot.add_cog(NewsNotice(bot))
