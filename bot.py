#! /usr/bin/env python3

import os
import re
import aiohttp
import signal
import sys

import discord
from discord import app_commands

from deep_translator import GoogleTranslator


try:
	TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError:
	print("ERROR: no token found! Please set the DISCORD_TOKEN env var!")
	sys.exit()


VERSION = "2.5"
EE_REBORN_GUILD = 614154073759023104
EE_REBORN_INVITE = "https://discord.gg/BjUXbFB"

dadjokeAPI = "https://icanhazdadjoke.com/"
darkjokeAPI = "https://v2.jokeapi.dev/joke/Dark?blacklistFlags=nsfw,religious,racist"

## Reactions on EE Reborn Server
EMPIREEARTHREBORN = "<:EmpireEarthReborn:614606364991291412>"
IKILLYOUREACTION = "<:Ikillyoureaction:708770715121352781>"
REALMANLYKNIFE = "<:REALMANLYKNIFE:750789564737519727>"
REALMANLYGUN = "<:REALMANLYGUN:1116855780042358875>"
REALMANLYGUN2 = "<:REALMANLYGUN2:1116855832890593381>"
BROKENASFUCK = "<:BROKENasFUCK:854865761994276874>"

SADREACTION = "<:sadreaction:663447982628143104>"
SERIOUSLYREACION = "<:seriouslyreaction:699029974245441616>"
CRAZYREACION = "<:crazyreaction:699029208462131312>"

EGGPLANT2 = "<:eggplant2:751522664044167188>"
DESPERATE_SHOT = "<:desperate_shot:751531469675167772>"
BULLET = "<:bullet:751529614987231266>"
PLUS18 = "<:18:740312683664113714>"

GETTHEFUCKOUT = "<:ZOCKERjustgetTHEFUCKOUT:854049905584504862>"

## EEReborn devteam user ping
AT_ATLAS = "<@536077018673053717>"

class FatherOfEE(discord.Client):

    GUILD_ID: int

    def __init__(self, guildID: int):
        # set requested permissions
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.guilds = True

        super().__init__(intents=intents)

        self.GUILD_ID = guildID
        self.guild = discord.Object(id=self.GUILD_ID) # self.get_guild(self.GUILD_ID)
        self.slashCommands = app_commands.CommandTree(self)

    def setupChannels(self):
        self.community_talk = self.get_channel(614157221902811240)
        self.bot_playground = self.get_channel(754680163475652629)
        self.welcome_channel = self.get_channel(614154073759023106)
        self.tech_support = self.get_channel(850300791335551026)
        self.test_channel = self.get_channel(751149878167601352)
        self.leave_channel = self.get_channel(832980373557870663)

    def setupTranslator(self):
        self.translator = GoogleTranslator(source='auto', target='en')
        print("translator ready!")

    async def setup_hook(self):
        #self.slashCommands.copy_global_to(guild=self.guild)
        #await self.slashCommands.sync(guild=self.guild)
        await super().setup_hook()

    async def on_ready(self):
        print("Logged in as", self.user, self.user.id)
        self.setupChannels()
        self.setupTranslator()

        # to get rid of zombie commands
        #self.slashCommands.clear_commands(guild=self.guild)

        syncedCommands = await self.slashCommands.sync()
        print("synced commands: ", [x.name for x in syncedCommands])

        await self.bot_playground.send(f"FATHER reports for duty with version {VERSION}!")

    #async def on_guild_remove()
    async def on_member_remove(self, member: discord.Member):
        try:
            banentry: discord.BanEntry = await member.guild.fetch_ban()

            await self.leave_channel.send(f"🔥🔥 Fucking {banentry.user.display_name} got banned!!! 🔥🔥")
            await self.leave_channel.send(f"Reason: {banentry.reason}")
            await self.leave_channel.send(GETTHEFUCKOUT+IKILLYOUREACTION)

        except discord.NotFound:
            await self.leave_channel.send(
                f"Fucking {member.display_name} left the server!!"
                " "+IKILLYOUREACTION+REALMANLYKNIFE+REALMANLYKNIFE,
                silent=True
            )

        except discord.Forbidden:
            print("Missing ~Permissions.ban_members permission")
        except discord.HTTPException as e:
            print("Failed to fetch_ban():", e)

    async def on_message(self, message: discord.Message):
        """
        this event only handles reactions and admin commands
        everything else uses slash commands
        """
        # don't react to own messages
        if message.author == self.user:
            return
        
        # print(message.content)

        ## join reaction

        if message.channel == self.welcome_channel:
            await message.add_reaction('👋')
            await message.add_reaction('👀')

        ## text reactions

        if re.match(r"^((I\s[a-z\s]*like\s|.*like(s)?)(beer).*|.*beer is.*)$", message.content.lower()):
            await message.channel.send("I LIKE BEER TOO!! 🍺🍻")

        if '<@753374754294988881>' in message.content:
            await message.channel.send(f"WHO PINGED ME?? {REALMANLYKNIFE}")

        if "FATHER" in message.content:
            await message.channel.send('HOW CAN I HELP?')

        eer = [ 'Reborn', 'reborn', 'EER' ]
        if any(x in message.content for x in eer):
            await message.add_reaction(EMPIREEARTHREBORN)

        #"egg" in message.content or "gun" in message.content or
        if re.match(r".*(pipe|pipes)(\s|\.|,|$)", message.content):
            await message.add_reaction(EGGPLANT2)

        if "father" in message.content or "Father" in message.content:
            await message.add_reaction(IKILLYOUREACTION)

        if "manly" in message.content or "MANLY" in message.content:
            await message.add_reaction(IKILLYOUREACTION)
            await message.add_reaction(REALMANLYGUN)
            await message.add_reaction(DESPERATE_SHOT)
            await message.add_reaction(BULLET)

        #if "rebellion" in message.content.lower():
        #    await message.channel.send("DID I HEAR REBELLION??")
        #    await message.channel.send("https://cdn.discordapp.com/attachments/535890577191862305/936410898803855380/but_animalsacrifice_04.png")

        if not message.content and \
                (message.channel == self.test_channel 
                or message.channel == self.get_channel(747077940092600371)):
            await message.add_reaction(EMPIREEARTHREBORN)
            await message.add_reaction(IKILLYOUREACTION)
            await message.add_reaction(SADREACTION)
            await message.add_reaction(SERIOUSLYREACION)
            await message.add_reaction(CRAZYREACION)

        nsfw = [ 'nsfw', 'NSFW', 'sexy' ]
        if any(x in message.content for x in nsfw):
            await message.add_reaction(PLUS18)

        if "night" in message.content or "sleep" in message.content:
            await message.add_reaction('😴')

        if "deer" in message.content or "dear" in message.content:
            await message.add_reaction('🦌')

        food = [ ' lunch', ' eat', ' food' ]
        if any(x in message.content for x in food):
            await message.add_reaction('🍔')
            await message.add_reaction('🥫')
            await message.add_reaction('🍖')
            await message.add_reaction('🐡')
            await message.add_reaction('🍺')

        if "beer" in message.content.lower():
            await message.add_reaction('🍺')
            await message.add_reaction('🍻')

        broken = [' ddraw.dll', 'error', 'crash', 'broken', 'not work', 'directx', 'fail', 'fuck']
        if message.channel in [self.tech_support, self.bot_playground, self.test_channel] \
             and any(x in message.content.lower() for x in broken):
            await message.add_reaction(BROKENASFUCK)


        ## sayc command
        if message.content.startswith("!sayc ") and message.channel == self.bot_playground:
            new_message = message.content.lower()[6:].strip()

            if new_message.endswith("."):
                new_message = new_message[:-1] + "!"

            if new_message.endswith("?"):
                new_message += "?"

            # not sure why I added that ffs
            #if new_message.endswith("father"):
            #    new_message = new_message[:-6]

            if len(new_message) <= 1:
                new_message = "what the heck should I say?!?"

            await self.community_talk.send(new_message.upper())

        ## test commands
        if message.channel == self.test_channel and message.content.startswith("!test"):
            try:
                await message.author.guild.fetch_ban(message.author)
            except discord.NotFound:
                print(message.author.display_name, "is not banned")
            except discord.Forbidden:
                print("Missing ~Permissions.ban_members permission")
            except discord.HTTPException as e:
                print("Failed to fetch_ban():", e)


def initSlashCommands(client: FatherOfEE):

    @client.slashCommands.command(name="hello", description="Say Hello!")
    async def hello(inter: discord.Interaction):
        await inter.response.send_message("Hello!")

    @client.slashCommands.command(name="helloatlasfield", description="Says hello to Atlasfield")
    async def helloAtlas(inter: discord.Interaction):
        await inter.response.send_message(f"Hello {AT_ATLAS}!")

    @client.slashCommands.command(name="badass")
    async def badass(inter: discord.Interaction):
        await inter.response.send_message(REALMANLYGUN2+IKILLYOUREACTION+REALMANLYGUN)

    @client.slashCommands.command(name="invite", description="shows invite link for this server")
    async def invite(inter: discord.Interaction):
        await inter.response.send_message(EE_REBORN_INVITE)

    @client.slashCommands.command(name="download", description="post download link of EE Reborn")
    #@client.slashCommands.command(name="releasedate", description="post release date of EE Reborn")
    async def download(inter: discord.Interaction):
        await inter.response.send_message("Looking for release date or download link??".upper())
        await inter.channel.send("https://cdn.discordapp.com/attachments/535891419655569410/824072629769076776/123.png")

    ## jokes

    @client.slashCommands.command(name="dadjoke")
    async def dadjoke(inter: discord.Interaction):
        print("fetching dadjoke...")
        async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
            async with session.get(dadjokeAPI) as resp:
                joke: dict = await resp.json()
                print(joke)
                await inter.response.send_message(f'Here is a _really_ bad dadjoke for you: \n\n **{joke.get("joke")}**')

    @client.slashCommands.command(name="darkjoke")
    async def darkjoke(inter: discord.Interaction):
        async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
            async with session.get(dadjokeAPI) as resp:
                data: dict = await resp.json()

                if data.get("type") == "twopart":
                    await inter.response.send_message(f'You requested a dark joke, so there you go: \n\n **{data.get("setup")}**\n\t**{data.get("delivery")}**')
                else:
                    await inter.response.send_message(f'You requested a dark joke, so there you go: \n\n **{data.get("joke")}**')

    ## say command

    @client.slashCommands.command(name="say", description="let FATHER say something!")
    @app_commands.describe(message="The message to say")
    async def say(inter: discord.Interaction, message: app_commands.Range[str, 1, None]):
        if message.endswith("."):
            message = message.replace(".", "!")

        if message.endswith("?"):
            message += "?"
        else:
            message += "!"

        await inter.response.send_message(message.upper())
        #await inter.channel.send(message.upper())

    ## translate command

    @client.slashCommands.command(name="translate", description="translates a message to English")
    @app_commands.describe(message="The message to translate")
    async def translate(inter: discord.Interaction, message: str):
        #print("message to translate:", message)

        org = discord.Embed(color=0xff00ff)
        org.add_field(name="original", value=message)
        trans = discord.Embed(color=0xff00ff)
        trans.add_field(name="translated", value=client.translator.translate(message))
        
        await inter.response.send_message(embeds=[org, trans])

        #banner = discord.Embed(color=0xff00ff)
        ## inter.message is None for some reason
        #banner.set_author(
        #    name=inter.message.author.display_name,
        #    icon_url=inter.message.author.avatar_url
        #)
        #banner.add_field(name="original", value=message)
        #banner.add_field(name="translated", value=client.translator.translate(message))
        #await inter.response.send_message(embed=banner)


    @client.slashCommands.command(name="ping")
    async def ping(inter: discord.Interaction):
        await inter.response.send_message("WHO PINGED ME???")


eeBot = FatherOfEE(EE_REBORN_GUILD)

initSlashCommands(eeBot)

## not needed anymore, discord.Client now has its own signal handler
#def end(*args):
#	print("trigger exit...")
#	eeBot.close()
#	sys.exit()
#signal.signal(signal.SIGTERM, end)
#signal.signal(signal.SIGINT, end)

eeBot.run(TOKEN)
