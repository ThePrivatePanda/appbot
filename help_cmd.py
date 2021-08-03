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
    @help.command(aliases=['slc'])
    async def set_log_channel(ctx):
        em = discord.Embed(title="set_log_channel command help", description="Detailed help on the `set_log_channel` command.")
        em.add_field(name="aliases", value="This command has one alias: `slc`", inline=False)
        em.add_field(name="Usage", value="This command will set the channel where logs will be written. Logs include commands used and status of applications.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the channel argument
            You can give the channel ID, or the channel mention:
            {get_prefix()}set_log_channel #channel
            {get_prefix()}set_log_channel channel_id
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['sac'])
    async def set_app_channel(ctx):
        em = discord.Embed(title="set_app_channel command help", description="Detailed help on the `set_app_channel` command.")
        em.add_field(name="aliases", value="This command has one alias: `sac`", inline=False)
        em.add_field(name="Usage", value="Set the channel where completed applications appear.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the channel argument
            You can give the channel ID, or the channel mention:
            {get_prefix()}set_app_channel #channel
            {get_prefix()}set_app_channel channel_id
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['add', 'aq', 'addq'])
    async def add_question(ctx):
        em = discord.Embed(title="`add_question` command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `add`, `aq` and `addq`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, those are, the category argument and the question itself
            You must give the exact name of the category, which also must be in single quotes:
            {get_prefix()}add_question 'dank' What prestige level are you?
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['rem', 'remove', 'rq'])
    async def rem_question(ctx):
        em = discord.Embed(title="`rem_question` command help", description="Detailed help on the `rem_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `rem`, `remove` and `remq`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category. Note: The question must be exactly as it appears.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, those are, the category argument and the question itself
            You must give the exact name of the category, which also must be in single quotes, and the question also must be exactly as it appears:
            {get_prefix()}rem_question 'dank' What prestige level are you?
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['bl'])
    async def whitelist(ctx):
        em = discord.Embed(title="`blacklist` command help", description="Detailed help on the `blacklist` command.")
        em.add_field(name="aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="Blacklist a role or user by id or mention, for a specific application or globally.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the user or role mention or id, and the second, which is optional, the name of the application:
            1. {get_prefix()}blacklist @role tmod
            2. {get_prefix()}blacklist user_id owner
            3. {get_prefix()}blacklist user_id
            
            Note: The third one will result in a global blacklist of the user
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['wl'])
    async def whitelist(ctx):
        em = discord.Embed(title="`whitelist` command help", description="Detailed help on the `whitelist` command.")
        em.add_field(name="aliases", value="This command has one alias: `wl`", inline=False)
        em.add_field(name="Usage", value="Whitelist a role or user by id or mention, for a specific application or globally.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the user or role mention or id, and the second, which is optional, the name of the application:
            1. {get_prefix()}whitelist @role tmod
            2. {get_prefix()}whitelist user_id owner
            3. {get_prefix()}wl user_id
            
            Note: The third one will result in a global whitelist of the user
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['ar'])
    async def add_req(ctx):
        em = discord.Embed(title="`add_req` command help", description="Detailed help on the `add_req` command.")
        em.add_field(name="aliases", value="This command has one alias: `ar`", inline=False)
        em.add_field(name="Usage", value="Add a role requirement to an application or globally", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the role mention or id, and the second, which is optional, the name of the application:
            1. {get_prefix()}add_req @role tmod
            2. {get_prefix()}add_req role_id owner
            3. {get_prefix()}ar role_id
            
            Note: The third one will result in role_id being a requirement for all applicatoins, i.e. a general req
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['rr'])
    async def rem_req(ctx):
        em = discord.Embed(title="`rem_req` command help", description="Detailed help on the `rem_req` command.")
        em.add_field(name="aliases", value="This command has one alias: `rr`", inline=False)
        em.add_field(name="Usage", value="Remove a role requirement to an application or globally", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the role mention or id, and the second, which is optional, the name of the application:
            1. {get_prefix()}rem_req @role tmod
            2. {get_prefix()}rem_req role_id owner
            3. {get_prefix()}rr role_id
            
            Note: The third one will result in role_id NO LONGER being a requirement for all applicatoins, i.e. a general req
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['ao'])
    async def add_owner(ctx):
        em = discord.Embed(title="`add_owner` command help", description="Detailed help on the `add_owner` command.")
        em.add_field(name="aliases", value="This command has one alias: `ao`", inline=False)
        em.add_field(name="Usage", value="Makes a user, the owner of the bot. This user will now be able to access ALL THE admin commands.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the user mention or id:
            1. {get_prefix()}add_owner @user
            2. {get_prefix()}ao user_id

            Note: Read the usage of this command again. Also requires bot restart to take effetc
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['ro'])
    async def rem_owner(ctx):
        em = discord.Embed(title="`rem_owner` command help", description="Detailed help on the `rem_owner` command.")
        em.add_field(name="aliases", value="This command has one alias: `ro`", inline=False)
        em.add_field(name="Usage", value="Removes a user from being a bot's owner.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the user mention or id:
            1. {get_prefix()}rem_owner @user
            2. {get_prefix()}ro user_id

            Note: Read the usage of this command again. Also requires bot restart to take effect.
            """, inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def accept(ctx):
        em = discord.Embed(title="`accept` command help", description="Detailed help on the `accept` command.")
        em.add_field(name="aliases", value="This command has no aliases.", inline=False)
        em.add_field(name="Usage", value="Accept a user's application.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            1. {get_prefix()}accept tmod @user be active
            2. {get_prefix()}accept owner user_id 
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['deny', 'decline'])
    async def reject(ctx):
        em = discord.Embed(title="`reject` command help", description="Detailed help on the `reject` command.")
        em.add_field(name="aliases", value="This command has two aliases: `deny`, `decline`", inline=False)
        em.add_field(name="Usage", value="Reject a user's application", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            1. {get_prefix()}reject tmod @user be active
            2. {get_prefix()}deny owner user_id 
            """, inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def consider(ctx):
        em = discord.Embed(title="`consider` command help", description="Detailed help on the `consider` command.")
        em.add_field(name="aliases", value="This command has no aliases.", inline=False)
        em.add_field(name="Usage", value="Consider a user's application", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            1. {get_prefix()}consider tmod @user I might accept you if you are active more
            2. {get_prefix()}consider gaw_man user_id donate more perhaps 
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['dump', 'questions', 'dumpq'])
    async def dump_questions(ctx):
        em = discord.Embed(title="`dump_questions` command help", description="Detailed help on the `dump_questions` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `questions`, and `dumpq`", inline=False)
        em.add_field(name="Usage", value="Returns the questions present in a category, if any.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the category argument which is optional
            You must give the exact name of the category:
            1. {get_prefix()}dump_questions dank
            2. {get_prefix()}dumpq

            Note: The second one will result in all the questions stored, being sent.
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['dumpr', 'requirements', 'reqs'])
    async def dump_req(ctx):
        em = discord.Embed(title="`dump_req` command help", description="Detailed help on the `dump_req` command.")
        em.add_field(name="aliases", value="This command has three aliases: `dump`, `requirements`, and `dumpr`", inline=False)
        em.add_field(name="Usage", value="Returns the requirements for a particulat application, if any.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the application argument which is optional
            You must give the exact name of the application:
            {get_prefix()}dump_questions tmod
            {get_prefix()}dumpq general

            Note: The second one will result in all the requirements stored, being sent.
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['sp', 'prefix'])
    async def set_prefix(ctx):
        em = discord.Embed(title="`set_prefix` command help", description="Detailed help on the `set_prefix` command.")
        em.add_field(name="aliases", value="This command has two aliases: `sp` and `prefix`", inline=False)
        em.add_field(name="Usage", value="Change the bot's prefix.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the new prefix:
            1. {get_prefix()}set_prefix ?!?
            2. {get_prefix()}sp !!

            Note: Ping the bot to know it's current prefix.
            """, inline=False)
        await ctx.send(embed=em)

    @help.command()
    async def toggle(ctx):
        em = discord.Embed(title="`toggle` command help", description="Detailed help on the `toggle` command.")
        em.add_field(name="aliases", value="This command has no aliases.", inline=False)
        em.add_field(name="Usage", value="toggle an application on and off", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, that is, on or off, and the app name:
            1. {get_prefix()}toggle off tmod
            2. {get_prefix()}toggle on owner
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['wh', 'hier'])
    async def write_hier(ctx):
        em = discord.Embed(title="`write_hier` command help", description="Detailed help on the `write_hier` command.")
        em.add_field(name="aliases", value="This command has two aliases: `wh` and `hier`.", inline=False)
        em.add_field(name="Usage", value="Write the application hierarchy.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is the rest of the entire message, in triple backticks, the new hierarchy:
            {get_prefix()}wh
            ```
            general:
                bot_mod:
                tmod:
            finishing:
            ```

            Note: This will result in first, the general questions being asked, then either bot_mod or tmod category questions, and lastly, the finishing category questions.
            The user will get a choice as to answer questions for bot_mod or tmod.
            """, inline=False)
        await ctx.send(embed=em)
