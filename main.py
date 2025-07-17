import os, discord, random, utils
from dotenv import load_dotenv

load_dotenv()

bot = discord.Bot()
hunter = "<@1104370538706632735>"
hunterSweetTalk = [f"Come back {hunter}, I miss you so much.", f"I will kill myself, {hunter}, if you don't come back.", f"{hunter}, the entirety of New Nameful yearns for your return."]

@bot.event
async def on_ready():
    print(f"{bot.user} has started.")

@bot.slash_command(name="pinghunter", description="Please come back forever :(")
async def pinghunter(ctx: discord.ApplicationContext):
    await ctx.respond(random.choice(hunterSweetTalk))

@bot.slash_command(name="election", description="Show New Nameful Election Info")
async def election(ctx: discord.ApplicationContext):
    await ctx.respond("The next election will start in " + str(utils.calculate_countdown(utils.get_json()["election"]["electionDate"])-7) + " days!\nThe new leaders will be appointed in " + str(utils.calculate_countdown(utils.get_json()["election"]["electionDate"])) + " days.")

bot.run(os.getenv("TOKEN"))
