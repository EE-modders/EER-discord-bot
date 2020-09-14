#! /usr/bin/env python3

"""
@autor: zocker_160

created: 09.09.2020 23:39

"""

import os
import discord

try:
	token = os.environ["DISCORD_TOKEN"]
except KeyError:
	print("ERROR: no token found! Please set the DISCORD_TOKEN env var!")
	exit()

client = discord.Client()

@client.event
async def on_ready():
	print('We have logged in as %s' % client.user)

	community_talk = client.get_channel(614157221902811240)
	print(community_talk)

	## function to write messages using the bot
	#
	#while True:
	#	msg = input("Inpout message:")
	#	await community_talk.send(msg)

@client.event
async def on_message(message):
	if message.author == client.user:
		return

	### direct commands

	if message.content.startswith('!hello'):
		await message.channel.send('Hello!')
        
	if message.content.startswith('!FATHER'):
		await message.channel.send('Hello <@536077018673053717>!')

	if message.content == 'my name is methos':
		await message.channel.send('FATHER is _MY_ name!! <:REALMANLYKNIFE:750789564737519727><:REALMANLYKNIFE:750789564737519727>')

	if message.content.startswith("!badass"):
		await message.channel.send('<:REALMANLYGUN2:749769945667338322><:Ikillyoureaction:708770715121352781><:REALMANLYGUN:749768825922257018>')
		#await message.channel.send('')

	if message.content == '!link' or message.content == '!invite':
		await message.channel.send('https://discord.gg/BjUXbFB')

	if message.content.startswith("!say") or message.content.startswith("!SAY"):
		redir_message = False
		new_message = message.content
		
		bot_playground = client.get_channel(754680163475652629)
		community_talk = client.get_channel(614157221902811240)
		
		if message.content.startswith("!sayc") and message.channel == bot_playground:
			redir_message = True
		
		# this sadly deletes too much....
		#await message.delete()
		
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


	### bot reactions

	if '<@!753374754294988881>' in message.content:
		await message.channel.send("WHO PINGED ME?? <:REALMANLYKNIFE:750789564737519727>")

	if "FATHER" in message.content:
		await message.channel.send('HOW CAN I HELP?')

	eer = [ ' EE', 'EE ', 'Empire Earth', 'Reborn', 'reborn', ' EEC', ' AoC' ]
	if any(x in message.content for x in eer):
		await message.add_reaction('<:EmpireEarthReborn:614606364991291412>')

	if "egg" in message.content or "gun" in message.content or "pipe" in message.content:
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
		#await message.add_reaction('🍲')
		await message.add_reaction('🥫')
		await message.add_reaction('🍺')

	if "beer" in message.content or "BEER" in message.content:
		await message.add_reaction('🍺')

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

client.run(token)
