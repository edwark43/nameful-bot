import discord, os, json, sys, heapq
sys.path.append("..")
import utils
from datetime import date
from discord.ext import commands, tasks
from dotenv.main import set_key, load_dotenv, find_dotenv

dotenv_path = find_dotenv("../.env")
load_dotenv(dotenv_path)

data = utils.get_json()

# class Poll():
#
#     def __init__(self, message):
#         self.logsChannel = self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID")))
#         self.message = message
#         return winnerPercentage
#
#     def get_candidates(self):
#         self.candidates = ""
#         for answer in self.message.poll.answers:
#             self.candidate=discord.utils.get(self.message.guild.members, name=answer.text.split("|")[0].split("(")[1].replace(" ", "")[:-1])
#             self.candidates += f"{{\"candidate\":\"{answer.text}\",\"avatar\":\"{self.candidate.avatar.url}\",\"voters\":\"{answer.count}\",\"percentage\":\"{str(answer.count/self.message.poll.total_votes()*100)}\"}},"
#         return self.candidates
#
#     def get_candidate_counts(self):
#         self.candidateCounts = []
#         for answer in self.message.poll.answers:
#             self.candidateCounts.append(answer.count)
#         return self.candidateCounts
#
#     def get_winner(self):
#         self.winner=discord.utils.get(self.message.guild.members, name=self.message.poll.get_answer(self.get_candidate_counts().index(max(self.get_candidate_counts()))+1).text.split("|")[0].split("(")[1].replace(" ", "")[:-1]) if self.message.poll.has_ended() else ""
#         return self.winner
#
#     def get_winner_percentage(self):
#         self.winnerPercentage=max(candidateCounts)/self.message.poll.total_votes()*100
#         return self.winnerPercentage
#
#     async def log_election(self):
#         self.jsonObject=json.loads(f"{{\"date\":\"{date.today().strftime('%B %Y')}\",\"question\":\"{self.message.poll.question.text.split('|')[0][:-1]}\",\"candidates\":[{self.get_candidates()[:-1]}]{f',\"winner\":{{\"candidate\":\"{self.get_winner().name}\",\"avatar\":\"{self.get_winner().avatar.url}\",\"voters\":\"{max(candidateCounts)}\",\"percentage\":\"{self.get_winner_percentage()}\"}}}}' if self.message.poll.has_ended() else '}'}")
#         if self.message.poll.has_ended():
#             data["election"]["pastElections"].append(jsonObject)
#             data["election"]["activeElection"] = "N/A"
#         else:
#             data["election"]["activeElection"] = jsonObject
#         os.remove(os.getenv("JSON"))
#
#         with open(os.getenv("JSON"), "w") as f:
#             json.dump(data, f, indent=2)
#         await logsChannel.send(json.dumps(jsonObject, indent=2))

class Election(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        if os.getenv("ELECTION_POLL_ACTIVE") == "True":
            self.check_poll_end_task.start()

    # async def log_election(self):
    #     logsChannel = self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID")))
    #     channel = self.bot.get_channel(int(os.getenv("POLLS_CHANNEL_ID")))
    #     message = await channel.fetch_message(int(os.getenv("ELECTION_POLL_ID")))
    #     candidates = ""
    #     candidateCounts = []
    #     for answer in message.poll.answers:
    #         candidate=discord.utils.get(message.guild.members, name=answer.text.split("|")[0].split("(")[1].replace(" ", "")[:-1])
    #         candidates += f"{{\"candidate\":\"{answer.text}\",\"avatar\":\"{candidate.avatar.url}\",\"voters\":\"{answer.count}\",\"percentage\":\"{str(answer.count/message.poll.total_votes()*100)}\"}},"
    #         candidateCounts.append(answer.count)
    #     winner=discord.utils.get(message.guild.members, name=message.poll.get_answer(candidateCounts.index(max(candidateCounts))+1).text.split("|")[0].split("(")[1].replace(" ", "")[:-1]) if message.poll.has_ended() else ""
    #     winnerPercentage=max(candidateCounts)/message.poll.total_votes()*100
    #     jsonObject=json.loads(f"{{\"date\":\"{date.today().strftime('%B %Y')}\",\"question\":\"{message.poll.question.text.split('|')[0][:-1]}\",\"candidates\":[{candidates[:-1]}]{f',\"winner\":{{\"candidate\":\"{winner.name}\",\"avatar\":\"{winner.avatar.url}\",\"voters\":\"{max(candidateCounts)}\",\"percentage\":\"{winnerPercentage}\"}}}}' if message.poll.has_ended() else '}'}")
    #     if message.poll.has_ended():
    #         data["election"]["pastElections"].append(jsonObject)
    #         data["election"]["activeElection"] = "N/A"
    #     else:
    #         data["election"]["activeElection"] = jsonObject
    #     os.remove(os.getenv("JSON"))
    #
    #     with open(os.getenv("JSON"), "w") as f:
    #         json.dump(data, f, indent=2)
    #     await logsChannel.send(json.dumps(jsonObject, indent=2))
    #     return winnerPercentage

    electionDate = discord.SlashCommandGroup("election-date", "Interact with Leader Data")

    @electionDate.command(name="get", description="Get Election Date Info")
    async def getElectionDate(self, ctx):
        await ctx.respond(f"The next election will start <t:{utils.calculate_countdown(data['election']['electionDate']) - 604800}:R>!", ephemeral=True)

    @electionDate.command(name="edit", description="Edit the Election Date on the Website (Format: mm/dd/YYYY)")
    @commands.guild_only()
    @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    async def editElectionDate(
            self,
            ctx,
            date: discord.Option(str)
            ):
        try:
            utils.calculate_countdown(date)
        except:
            await ctx.respond("Error: Incorrect date format. Correct format: mm/dd/YYYY", ephemeral="True")
        else:
            data["election"]["electionDate"] = date

            os.remove(os.getenv("JSON"))
        
            with open(os.getenv("JSON"), "w") as f:
                json.dump(data, f, indent=2)

                await ctx.respond(f"Changed election date to {date}.", ephemeral="True")

    # @discord.slash_command(name="start-mock-election", description="guh")
    # @commands.guild_only()
    # @commands.has_role(int(os.getenv("ADMIN_ROLE_ID")))
    # async def mockElection(self, ctx):
    #     logsChannel = self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID")))
    #     channel = self.bot.get_channel(int(os.getenv("ANNOUNCEMENTS_CHANNEL_ID")))
    #     poll = discord.Poll(
    #             question=f"New Nameful Election Candidacy Application | {date.today().strftime('%B %Y')}",
    #             answers=[discord.PollAnswer("I Apply.")],
    #             duration=24
    #             )
    #
    #     await ctx.respond("done", ephemeral=True)
    #     await channel.send("||`@everyone`||\n**(MOCK)**\nPlease vote on the following poll if you would like to apply for candidacy in the upcoming elections.")
    #     poll = await channel.send(poll=poll)
    #     # await logsChannel.send(ctx.user.id)
    #
    #     self.check_poll_end_task.start()
    #
    #     set_key(dotenv_path, "ELECTION_POLL_ID", str(poll.id))
    #     set_key(dotenv_path, "ELECTION_POLL_ACTIVE", "True")
    #
    # @discord.slash_command(name="declare-running-mate", description="Declare your running mate.")
    # @commands.guild_only()
    # @commands.has_role(int(os.getenv("CANDIDATE_ROLE_ID")))
    # async def declareRunningMate(
    #         self,
    #         ctx,
    #         user: discord.Option(discord.SlashCommandOptionType.user, "Choose your running mate")
    #         ):
    #     if os.getenv("ELECTION_POLL_ACTIVE") == "True":
    #         try: 
    #             message = await announcementsChannel.fetch_message(int(os.getenv("ELECTION_POLL_ID")))
    #         except:
    #             await ctx.respond("The time to declare a running mate has passed.", ephemeral=True)
    #         else:
    #             load_dotenv(dotenv_path,override=True)
    #             try:
    #                 candidate = os.getenv("CANDIDATES").split(",").index(str(ctx.user.id))
    #                 runningMate = os.getenv("CANDIDATES").split(",")[candidate]
    #                 set_key(dotenv_path, "RUNNING_MATES", os.getenv("RUNNING_MATES").replace(runningMate, str(user.id)))
    #                 await ctx.respond(f"Changed your running mate to {user.name}.", ephemeral=True)
    #             except:
    #                 if os.getenv("CANDIDATES").split(",") == ['']:
    #                     set_key(dotenv_path, "CANDIDATES", str(ctx.user.id))
    #                     set_key(dotenv_path, "RUNNING_MATES", str(user.id))
    #                     await ctx.respond(f"Set your running mate to {user.name}.", ephemeral=True)
    #                 else:
    #                     set_key(dotenv_path, "CANDIDATES", f"{os.getenv('CANDIDATES')},{ctx.user.id}")
    #                     set_key(dotenv_path, "RUNNING_MATES", f"{os.getenv('RUNNING_MATES')},{user.id}")
    #                     await ctx.respond(f"Set your running mate to {user.name}.", ephemeral=True)
    #     else:
    #         await ctx.respond("There is no currently running election.", ephemeral=True)
    #
    # @commands.Cog.listener()
    # async def on_raw_poll_vote_add(self, payload):
    #     load_dotenv(dotenv_path,override=True)
    #
    #     channel = self.bot.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     answer = message.poll.get_answer(payload.answer_id)
    #
    #     await self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID"))).send(f"User \"{self.bot.get_user(payload.user_id).name}\" ({payload.user_id}) voted for Answer \"{answer.text}\" ({answer.id}) on Poll \"{message.poll.question.text}\" ({payload.message_id})")
    #     if message.poll.question.text == f"New Nameful Election Candidacy Application | {date.today().strftime('%B %Y')}":
    #         await message.guild.get_member(payload.user_id).add_roles(message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))))
    #     elif message.poll.question.text == f"New Nameful Rulership Election | {date.today().strftime('%B %Y')}":
    #         await self.log_election()
    #     await message.poll.end()
    #
    # @commands.Cog.listener()
    # async def on_raw_poll_vote_remove(self, payload):
    #     load_dotenv(dotenv_path,override=True)
    #
    #     channel = self.bot.get_channel(payload.channel_id)
    #     message = await channel.fetch_message(payload.message_id)
    #     answer = message.poll.get_answer(payload.answer_id)
    #
    #     await self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID"))).send(f"User \"{self.bot.get_user(payload.user_id).name}\" ({payload.user_id}) removed vote for Answer \"{answer.text}\" ({answer.id}) on Poll \"{message.poll.question.text}\" ({payload.message_id})")
    #     if message.poll.question.text == f"New Nameful Election Candidacy Application | {date.today().strftime('%B %Y')}":
    #         await message.guild.get_member(payload.user_id).remove_roles(message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))))
    #     elif message.poll.question.text == f"New Nameful Rulership Election | {date.today().strftime('%B %Y')}":
    #         await self.log_election()
    #
    # @tasks.loop(seconds=5)
    # async def check_poll_end_task(self):
    #     load_dotenv(dotenv_path,override=True)
    #
    #     logsChannel = self.bot.get_channel(int(os.getenv("LOGS_CHANNEL_ID")))
    #     announcementsChannel = await self.bot.fetch_channel(int(os.getenv("ANNOUNCEMENTS_CHANNEL_ID")))
    #     pollsChannel = await self.bot.fetch_channel(int(os.getenv("POLLS_CHANNEL_ID")))
    #
    #     if os.getenv("ELECTION_POLL_ACTIVE") == "True":
    #         try: 
    #             message = await announcementsChannel.fetch_message(int(os.getenv("ELECTION_POLL_ID")))
    #         except:
    #             message = await pollsChannel.fetch_message(int(os.getenv("ELECTION_POLL_ID")))
    #         if message.poll.has_ended():
    #             if message.poll.question.text == f"New Nameful Election Candidacy Application | {date.today().strftime('%B %Y')}":
    #                 answer = message.poll.get_answer(1)
    #                 poll = discord.Poll(
    #                         question=f"New Nameful Rulership Election | {date.today().strftime('%B %Y')}",
    #                         duration=72
    #                         )
    #                 async for user in answer.voters():
    #                     runningMate = ""
    #                     try:
    #                         runningMate = self.bot.get_user(int(os.getenv("RUNNING_MATES").split(",")[os.getenv("CANDIDATES").split(",").index(str(user.id))])).display_name
    #                     except:
    #                         runningMate = ""
    #                     poll.add_answer(f"{user.display_name.replace('|', '').replace('(', '')} ({user.name}) ({user.roles[1]}){f' | {runningMate}' if runningMate != '' else ''}")
    #                 await pollsChannel.send(f"||`@everyone`||\n**(MOCK)**\nThe rulership elections for {date.today().strftime('%B')} have officially began!\nCandidates may not vote for themselves.")
    #                 poll = await pollsChannel.send(poll=poll)
    #                 set_key(dotenv_path, "ELECTION_POLL_ID", str(poll.id))
    #             elif message.poll.question.text == f"New Nameful Rulership Election | {date.today().strftime('%B %Y')}":
    #                 winnerPercentage = await self.log_election()
    #                 if round(winnerPercentage) <= 33 or os.getenv("OVERRIDE_RUNOFFS") == "True":
    #                     poll = discord.Poll(
    #                             question=f"New Nameful Rulership Election Runoffs | {date.today().strftime('%B %Y')}",
    #                             duration=72
    #                             )
    #                     answerCounts = []
    #                     for answer in message.poll.answers:
    #                         answerCounts.append(answer.count)
    #                         for num in heapq.nlargest(2, answerCounts):
    #                             poll.add_answer(message.poll.answers[answerCounts.index(num)].text)
    #                     await pollsChannel.send(f"||`@everyone`||\n**(MOCK)**\nSince no candidate recieved a voter count greater than 33%, election runoffs for {date.today().strftime('%B')} have begun.\nYou may only participate in the runoffs if you participated in the main election and all main election rules still apply.")
    #                     poll = await pollsChannel.send(poll=poll)
    #                     set_key(dotenv_path, "ELECTION_POLL_ID", str(poll.id))
    #                 else:
    #                     self.check_poll_end_task.stop()
    #                     set_key(dotenv_path, "ELECTION_POLL_ACTIVE", "False")
    #                     for member in message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))).members:
    #                         await member.remove_roles(message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))))
    #                     set_key(dotenv_path, "CANDIDATES", "")
    #                     set_key(dotenv_path, "RUNNING_MATES", "")
    #
    #             else:
    #                 await self.log_election()
    #                 self.check_poll_end_task.stop()
    #                 set_key(dotenv_path, "ELECTION_POLL_ACTIVE", "False")
    #                 for member in message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))).members:
    #                     await member.remove_roles(message.guild.get_role(int(os.getenv("CANDIDATE_ROLE_ID"))))
    #                 set_key(dotenv_path, "CANDIDATES", "")
    #                 set_key(dotenv_path, "RUNNING_MATES", "")


def setup(bot):
    bot.add_cog(Election(bot))
