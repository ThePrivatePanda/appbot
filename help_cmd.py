import discord
from discord.ext import commands
bot = commands.Bot

def get_prefix():
    with open(r"config\prefix.txt") as file:
        return file.read()

def help_cmd():
    @bot.group(invoke_without_command=True)
    async def help(ctx):
        em = discord.Embed(title="Help Page", description=f"use {get_prefix()}help <command> for a more detailed help on the command.")
        em.add_field(
            name="Admin Commands", 
            value=("""
                1) set_log_channel
                2) set_app_channel
                3) add_question
                4) rem_question
                5) blacklist
                6) whitelist
                7) add_req
                8) remove_req
                9) global_blacklist
                10) global_whitelist
                11) add_owner
                12) rem_owner
                13) set_prefix
                13) toggle
                14) dump_questions
                15) write_hier
                """))
        em.add_field(name="Public Commands", value="""
                1) help
                2) apply
                3) raise_er
                """)
        await ctx.send(embed=em)
    @help.command()
    async def set_log_channel(ctx):
        em = discord.Embed(title="set_log_channel command help", description="Detailed help on the `set_log_channel` command.")
        em.add_field(name="aliases", value="This command has one alias: `slc`", inline=False)
        em.add_field(name="Usage", value="This command will set the channel where logs will be written. Logs include commands used and status of applications.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the channel argument\nYou can give the channel ID, or the channel mention:\n{get_prefix()}set_log_channel #channel\nn{get_prefix()}set_log_channel channel_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def slc(ctx):
        em = discord.Embed(title="set_log_channel command help", description="Detailed help on the `set_log_channel` command.")
        em.add_field(name="aliases", value="This command has one alias: `slc`", inline=False)
        em.add_field(name="Usage", value="This command will set the channel where logs will be written. Logs include commands used and status of applications.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the channel argument\nYou can give the channel ID, or the channel mention:\n{get_prefix()}slc #channel\nn{get_prefix()}slc channel_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def dump_questions(ctx):
        em = discord.Embed(title="dump_questions command help", description="Detailed help on the `dump_questions` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `questions`, and `dumpq`", inline=False)
        em.add_field(name="Usage", value="Returns the questions present in a category, if any.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the category argument\You must give the exact name of the category: {get_prefix()}dump_questions dank", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def dump(ctx):
        em = discord.Embed(title="dump_questions command help", description="Detailed help on the `dump_questions` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `questions`, and `dumpq`", inline=False)
        em.add_field(name="Usage", value="Returns the questions present in a category, if any.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the category argument\You must give the exact name of the category: {get_prefix()}dump dank", inline=False)
        await ctx.send(embed=em)
    @help.command
    async def dumpq(ctx):
        em = discord.Embed(title="dump_questions command help", description="Detailed help on the `dump_questions` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `questions`, and `dumpq`", inline=False)
        em.add_field(name="Usage", value="Returns the questions present in a category, if any.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the category argument\You must give the exact name of the category: {get_prefix()}dumpq dank", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def questions(ctx):
        em = discord.Embed(title="dump_questions command help", description="Detailed help on the `dump_questions` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `questions`, and `dumpq`", inline=False)
        em.add_field(name="Usage", value="Returns the questions present in a category, if any.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the category argument\You must give the exact name of the category: {get_prefix()}questions dank", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def add_question(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `ad`, and `add`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before..", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes: {get_prefix()}add_question 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def ad(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `ad`, and `add`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before..", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes: {get_prefix()}ad 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def add(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `ad`, and `add`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before..", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes: {get_prefix()}add 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def rem_question(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `rem`, and `remove`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes, and the question also must be exactly as it appears: {get_prefix()}rem_question 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def rem(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `rem`, and `remove`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes, and the question also must be exactly as it appears: {get_prefix()}rem 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def remove(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has two aliases: `rem`, and `remove`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, those are, the category argument and the question itself\You must give the exact name of the category, which also must be in single quotes, and the question also must be exactly as it appears: {get_prefix()}remove 'dank' What prestige level are you? ", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def set_app_channel(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `set_app_channel` command.")
        em.add_field(name="aliases", value="This command has one alias: `sac`", inline=False)
        em.add_field(name="Usage", value="Set the channel where completed applications appear.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the channel argument\nYou can give the channel ID, or the channel mention:\n{get_prefix()}set_app_channel #channel\nn{get_prefix()}set_app_channel channel_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def sac(ctx):
        em = discord.Embed(title="add_question command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has one alias: `sac`", inline=False)
        em.add_field(name="Usage", value="Set the channel where completed applications appear.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes a single argument, that is, the channel argument\nYou can give the channel ID, or the channel mention:\n{get_prefix()}sac #channel\nn{get_prefix()}sac channel_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def blacklist(ctx):
        em = discord.Embed(title="blacklist command help", description="Detailed help on the `blacklist` command.")
        em.add_field(name="aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="Blacklist a role or user by id or mention, for a specific application.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, that is, the name of the application and the ID argument\nYou can mention the user/role, or give the user/role ID:\n{get_prefix()}blacklist tmod @role\n{get_prefix()}blacklist gaw_manager user_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def bl(ctx):
        em = discord.Embed(title="blacklist command help", description="Detailed help on the `blacklist` command.")
        em.add_field(name="aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="Blacklist a role or user by id or mention, for a specific application.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, that is, the name of the application and the ID argument\nYou can mention the user/role, or give the user/role ID:\n{get_prefix()}bl tmod @role\n{get_prefix()}bl gaw_manager user_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def whitelist(ctx):
        em = discord.Embed(title="whitelist command help", description="Detailed help on the `whitelist` command.")
        em.add_field(name="aliases", value="This command has one alias: `wl`", inline=False)
        em.add_field(name="Usage", value="whitelist a role or user by id or mention, for a specific application.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, that is, the name of the application and the ID argument\nYou can mention the user/role, or give the user/role ID:\n{get_prefix()}whitelist tmod @role\n{get_prefix()}whitelist gaw_manager user_id", inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def wl(ctx):
        em = discord.Embed(title="whitelist command help", description="Detailed help on the `whitelist` command.")
        em.add_field(name="aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="whitelist a role or user by id or mention, for a specific application.", inline=False)
        em.add_field(name="Syntax", value=f"This command takes two arguments, that is, the name of the application and the ID argument\nYou can mention the user/role, or give the user/role ID:\n{get_prefix()}wl tmod @role\n{get_prefix()}wl gaw_manager user_id", inline=False)
        await ctx.send(embed=em)

help_cmd()
