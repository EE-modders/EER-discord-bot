#! /usr/bin/env python3

"""
@autor: zocker_160

created: 09.09.2020 23:39

"""

import os
import re
import aiohttp
import signal
import sys

import discord

from deep_translator import GoogleTranslator

dadjokeAPI = "https://icanhazdadjoke.com/"
darkjokeAPI = "https://v2.jokeapi.dev/joke/Dark?blacklistFlags=nsfw,religious,racist"

VERSION = "1.11"

try:
	TOKEN = os.environ["DISCORD_TOKEN"]
except KeyError:
	print("ERROR: no token found! Please set the DISCORD_TOKEN env var!")
	sys.exit()

	
print("connecting...")
client = discord.Client()
print("client connected!")

translator = GoogleTranslator(source='auto', target='en')
print("translator ready!")

async def end():
	print("trigger exit...")
	client.close()
	sys.exit()

signal.signal(signal.SIGTERM, end)
signal.signal(signal.SIGINT, end)

async def send_dadjoke(channel: discord.TextChannel):
	print("fetching dadjoke...")
	async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
		async with session.get(dadjokeAPI) as resp:
			joke: dict = await resp.json()
			print(joke)
			await channel.send(f'Here is a _really_ bad dadjoke for you: \n\n **{joke.get("joke")}**')

async def send_darkjoke(channel: discord.TextChannel):
	print("fetching dark joke...")
	async with aiohttp.ClientSession(headers={"Accept": "application/json"}) as session:
		async with session.get(dadjokeAPI) as resp:
			data: dict = await resp.json()

			if data.get("type") == "twopart":
				await channel.send(f'You requested a dark joke, so there you go: \n\n **{data.get("setup")}**\n\t**{data.get("delivery")}**')
			else:
				await channel.send(f'You requested a dark joke, so there you go: \n\n **{data.get("joke")}**')

@client.event
async def on_ready():
	print('We have logged in as', client.user)

	global community_talk
	global bot_playground
	global welcome_channel
	global tech_support
	global test_channel

	community_talk = client.get_channel(614157221902811240)
	bot_playground = client.get_channel(754680163475652629)
	welcome_channel = client.get_channel(614154073759023106)
	tech_support = client.get_channel(850300791335551026)
	test_channel = client.get_channel(751149878167601352)

	#print(community_talk)

	await bot_playground.send(f"FATHER reports for duty with version {VERSION}!")

	## function to write messages using the bot
	#
	#while True:
	#	msg = input("Inpout message:")
	#	await community_talk.send(msg)

@client.event
async def on_member_remove(member: discord.Member):
	leave_channel: discord.TextChannel = client.get_channel(832980373557870663)
	await leave_channel.send(f'Fucking {member.display_name} left the server!!')
	await leave_channel.send('<:Ikillyoureaction:708770715121352781><:REALMANLYKNIFE:750789564737519727><:REALMANLYKNIFE:750789564737519727>')

@client.event
async def on_message(message: discord.Message):
	if message.author == client.user:
		return

	### join reactions
	if message.channel == welcome_channel:
		await message.add_reaction('👋')
		await message.add_reaction('👀')

	### direct commands
	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')
        
	if message.content.startswith('!FATHER'):
		await message.channel.send('Hello <@536077018673053717>!')

	if message.content == 'my name is methos':
		await message.channel.send('FATHER is _MY_ name!! <:REALMANLYKNIFE:750789564737519727><:REALMANLYKNIFE:750789564737519727>')

	if message.content.startswith("!badass"):
		await message.channel.send('<:REALMANLYGUN2:749769945667338322><:Ikillyoureaction:708770715121352781><:REALMANLYGUN:749768825922257018>')

	if message.content == '!link' or message.content == '!invite':
		await message.channel.send('https://discord.gg/BjUXbFB')

	if message.content in ['!release', '!date', '!download'] and message.content.startswith('!'):
		await message.channel.send("Looking for release date or download link??".upper())
		await message.channel.send('https://cdn.discordapp.com/attachments/535891419655569410/824072629769076776/123.png')

	## jokes
	if message.content.startswith("!dadjoke") or re.match(r".*(father|please|tell).*(\sme\s).*(dad\s?joke).*$", message.content.lower()):
		await send_dadjoke(message.channel)

	if message.content.startswith("!darkjoke") or re.match(r".*(father|please|tell).*(\sme\s).*(dark\s?joke).*$", message.content.lower()):
		await send_darkjoke(message.channel)


	if re.match(r"^((I\s[a-z\s]*like\s|.*like(s)?)(beer).*|.*beer is.*)$", message.content.lower()):
		await message.channel.send("I LIKE BEER TOO!! 🍺🍻")

	## say command
	if message.content.lower().startswith("!say"):
		redir_message = False
		new_message = message.content
		
		if message.content.lower().startswith("!sayc") and message.channel == bot_playground:
			redir_message = True
		
		end = "!"
		if new_message.endswith(".") or new_message.endswith("!"):
			new_message = new_message[5:-1]
		elif new_message.endswith("?"):
			new_message = new_message[5:-1]
			end = "?"
		else:
			new_message = new_message[5:]

		if new_message.endswith("father") or new_message.endswith("FATHER"):
			new_message = new_message[:-6]

		new_message = new_message.upper() + end

		if redir_message:
			await community_talk.send(new_message[1:]) # I need to cut away the first letter, since "sayc" is longer by one char
		else:
			await message.channel.send(new_message)

	## translate command
	if message.content.lower().startswith("!t "):
		msg: str = message.content[3:]

		banner = discord.Embed(
			title="",
			description=translator.translate(msg),
			color=0xff00ff
		)
		banner.set_author(
			name=message.author.display_name,
			icon_url=message.author.avatar_url
		)
		#banner.set_footer(text="FATHER's best translator")

		await message.channel.send(embed=banner)

	### bot reactions
	if '<@!753374754294988881>' in message.content:
		await message.channel.send("WHO PINGED ME?? <:REALMANLYKNIFE:750789564737519727>")

	if "FATHER" in message.content:
		await message.channel.send('HOW CAN I HELP?')

	eer = [ 'Reborn', 'reborn', 'EER' ]
	if any(x in message.content for x in eer):
		await message.add_reaction('<:EmpireEarthReborn:614606364991291412>')

	#"egg" in message.content or "gun" in message.content or
	if re.match(r".*(pipe|pipes)(\s|\.|,|$)", message.content):
		await message.add_reaction('<:eggplant2:751522664044167188>')

	if "father" in message.content or "Father" in message.content:
		await message.add_reaction('<:Ikillyoureaction:708770715121352781>')

	if "manly" in message.content or "MANLY" in message.content:
		await message.add_reaction('<:Ikillyoureaction:708770715121352781>')
		await message.add_reaction('<:REALMANLYGUN:749768825922257018>')
		await message.add_reaction('<:desperate_shot:751531469675167772>')
		await message.add_reaction('<:bullet:751529614987231266>')

	if not message.content and (message.channel == client.get_channel(751149878167601352) or message.channel == client.get_channel(747077940092600371)):
		await message.add_reaction('<:EmpireEarthReborn:614606364991291412>')
		await message.add_reaction('<:Ikillyoureaction:708770715121352781>')
		await message.add_reaction('<:sadreaction:663447982628143104>')
		await message.add_reaction('<:seriouslyreaction:699029974245441616>')
		await message.add_reaction('<:crazyreaction:699029208462131312>')

	nsfw = [ 'nsfw', 'NSFW', 'sexy' ]
	if any(x in message.content for x in nsfw):
		await message.add_reaction('<:18:740312683664113714>')

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
	if message.channel in [tech_support, bot_playground, test_channel] and \
			any(x in message.content.lower() for x in broken):
		await message.add_reaction('<:BROKENasFUCK:854865761994276874>')

	## admin only functions
	"""
	if message.content == "!clean":
		testchannel = client.get_channel(747077940092600371)

		async for message in testchannel.history():
			tmp_content = message.content
			if tmp_content:
				await message.delete()
				print("deleted: %s" % tmp_content)
			else:
				print("skipped")

		await testchannel.send("CLEANUP DONE!")

	if message.content == "!cleanall":
		async for message in message.channel.history():
			tmp_content = message.content
			await message.delete()
			print("deleted: %s" % tmp_content)

		await message.channel.send("CLEANUP DONE!")

	if message.content == "!copy":
		dest_channel = client.get_channel(753548034515664906)
		#bot_playground = client.get_channel(753548034515664906)
		#old_wips = client.get_channel(615334191436922901)

		async for message in message.channel.history(limit=None, oldest_first=True):
			if message.author == client.user:
				continue
			if message.content:
				await dest_channel.send("**<%s>** %s:\n %s" % (message.author, str(message.created_at)[:-7], message.content))
			else:
				for file in message.attachments:
					await dest_channel.send("**<%s>** %s:\n %s" % (message.author, str(message.created_at)[:-7], file.url))
					
		await message.channel.send("COPY DONE!")

	if message.content == "!copyimages":
		dest_channel = client.get_channel(747077940092600371)
		#bot_playground = client.get_channel(753548034515664906)
		#old_wips = client.get_channel(615334191436922901)

		async for message in message.channel.history(limit=None, oldest_first=True):
			if message.author == client.user:
				continue
			if not message.content:
				for file in message.attachments:
					if "tenor.com" not in file.url:
						await dest_channel.send("**<%s>** %s:\n %s" % (message.author, str(message.created_at)[:-7], file.url))
					
		await message.channel.send("COPY DONE!")
	"""

client.run(TOKEN)
