import discord
from discord.ext import commands
from discord.utils import find

import os, traceback, sys
from random import randint, choice

from functions import ClientError, ComError, CooldownError, ExistError, ParamError, SendDM, getComEmbed

import json
with open('./data/profiles.json') as file:
	PROFILES = json.load(file)

# My Son.
class NotAidanBot(commands.Bot):
	def __setitem__(self, key, value):
		setattr(self, key, value)
	def __getitem__(self, key):
		return getattr(self, key)

	def getprefix(self, selfagain, message):
		return self.prefix

	def __init__(self):
		self.version = "Only Version (I'm too good)"

		intents = discord.Intents.all()
		super().__init__(command_prefix=self.getprefix, case_insensitive=True, help_command=None, intents=intents, allowed_mentions=discord.AllowedMentions(everyone=False, roles=False))

		for filename in os.listdir('./cogs'):
			if filename.endswith('.py') and not filename.startswith('_'):
				self.load_extension(f'cogs.{filename[:-3]}')

	async def on_ready(self):
		for name in PROFILES["main"]:
			self[name] = PROFILES["main"][name]

		await self.change_presence(activity=discord.Activity(name=f"The Best Bot Eva!",type=discord.ActivityType.playing))
		print(f"< Logged in: {self.user.name} >")

	# events #

	async def on_message(self, message):
		ctx = await self.get_context(message)
		if (not self.is_ready()) or message.webhook_id or ctx.author.id == self.user.id:
			return
		# fun stuff
		if (not ctx.command) and randint(1,10) == 10:
			phrases = ["I AM THE BEST BOT EVA!", "PLEASE USE ME", "I AM SOO COOL", "USE -HELP FOR HELP!"]
			return await ctx.send(choice(phrases))
		if message.content.startswith("$"):
			await ctx.send("AHAHHAHAHA, No thanks, AidanBot isn't here anymore...")

		await self.invoke(ctx)

	async def on_command_error(self, ctx, error):
		if isinstance(error, discord.ClientException):
			await ClientError(ctx, self, error)
		elif isinstance(error, commands.CommandOnCooldown):
			await CooldownError(ctx, self, error)
		elif isinstance(error, commands.MissingRequiredArgument):
			await ParamError(ctx, self, error)
		elif isinstance(error, commands.CommandNotFound):
			await ExistError(ctx, self)
		else:
			await ComError(ctx, self, error)
			if await self.is_owner(ctx.author):
				print('Ignoring exception in command {}:'.format(ctx.command), file=sys.stderr)
				traceback.print_exception(type(error), error, error.__traceback__, file=sys.stderr)