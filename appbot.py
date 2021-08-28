import asyncio, discord, os, sys
from discord.errors import Forbidden, HTTPException, NotFound
from discord.ext import commands
from collections import Counter
from typing import Union
import random

blue=0x1F51FF
red=0xFF2400
green=0x00FF7F
token = sys.argv[1]

em = discord.Embed(title="Test Embed", description="Just ensuring i can send messages and embeds here", colour=random.choice([green, blue, 0x02dcff]))

def get_prefix():
    with open(r"config\prefix.txt") as file:
        return file.read()
def get_owners():
    t = []
    with open(r"config\owners.txt") as file:
        ax = file.readlines()
        for ay in ax:
            if ay != "" and len(ay.replace("\n", "")) == 18:
                t.append(int(ay.replace("\n", "")))
        return t

bot = commands.Bot(command_prefix=get_prefix(), owner_ids=get_owners())
bot.remove_command('help')
bot.case_insensitive = True

def get_reg_log_channel():
    with open(r"config\logch.txt") as file:
        x = int(file.read())
    return x

async def log(content, ctx=None, colour=None):

    if colour is None:
        colour = 0x02dcff
    if ctx is not None:
        dsc_content = discord.Embed(title=f"{ctx.author.id} | {ctx.author.name}", description=content, colour=colour)
        content = f"{ctx.author.id} | {ctx.author.name} | {content}"
    else:
        content = f"{content}\n"
        dsc_content = discord.Embed(title=f"None", description=content, colour=colour)


    try:
        with open(r"config\reg_log.txt", "a") as file:
            file.write(content)
        x = get_reg_log_channel()
        ch = bot.get_channel(x)
        if ch != None:
            await ch.send(embed=dsc_content)
            return
        else:
            ch = bot.fetch_channel(x)
            if ch != None:
                await ch.send(embed=dsc_content)
                return
    except Exception as e:
        print(e)

def get_version():
    with open(r"config\version.txt") as file:
        return file.read().replace("\n", "")

def write_version():
    z = int(get_version())
    with open(r"config\version.txt", "w") as file:
        file.write(f"{z+1}")

@bot.event
async def on_ready():
    print("logged in")
    write_version()
    ch = await bot.fetch_channel(get_last_channel())
    await ch.send(f"Came online with version: {get_version()}")
    await asyncio.create_task(log(f"Came online with version: {get_version()}"))
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Game(name="not a joke."))


@bot.listen()
async def on_message(msg):
    pass

##########################################################################
################################## Help ##################################
################################# Command ################################
##########################################################################
def help_cmd():
    @bot.group(invoke_without_command=True)
    async def help(ctx):
        em = discord.Embed(title="Help Page", description=f"use {get_prefix()}help <command> for a more detailed help on the command.")
        em.add_field(
            name="Admin Commands", 
            value=("""
                1) set_log_channel: slc, setlog
                2) set_app_channel: sac, setapp
                3) add_question: add, aq, addq
                4) rem_question: rem, remove, rq, remq
                5) blacklist: bl
                6) whitelist: wl
                7) add_req: ar, addreq
                8) remove_req: rr, remreq
                9) add_owner: ao
                10) rem_owner: ro
                11) accept
                12) reject: deny, decline
                13) consider
                14) dump_questions: dump, questions, dumpq
                15) dump_req:dump1, requirements, reqs
                16) set_prefix: sp, prefix
                17) toggle
                18) write_hier: wh, hier
                """))
        em.add_field(name="Public Commands", value="""
                1) help
                2) apply
                3) raise_er
                """)
        await ctx.send(embed=em)

    # SET CONFIG COMMANDS
    @help.command(aliases=['slc', 'setlog'])
    async def set_log_channel(ctx):
        em = discord.Embed(title="`set_log_channel` command help", description="Detailed help on the `set_log_channel` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `slc` and `setlog`", inline=False)
        em.add_field(name="Usage", value="This command will set the channel where logs will be written. Logs include commands used and status of applications. Takes a single `channel` argument.", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}set_log_channel [ #channel | channel_id ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    @help.command(aliases=['sac', 'setapp'])
    async def set_app_channel(ctx):
        em = discord.Embed(title="`set_app_channel` command help", description="Detailed help on the `set_app_channel` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `sac` and `setapp`", inline=False)
        em.add_field(name="Usage", value="Set the channel where completed applications appear. Takes a single `channel` argument.", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}set_app_channel [ #channel | channel_id ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    # QUESTION MANAGEMENT COMMANDS
    @help.command(aliases=['add', 'aq', 'addq'])
    async def add_question(ctx):
        em = discord.Embed(title="`add_question` command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `add`, `aq` and `addq`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before. Takes two arguments, `category` and `question`", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}add_question [ category ] [ question ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    @help.command(aliases=['rem', 'remove', 'rq', 'remq'])
    async def rem_question(ctx):
        em = discord.Embed(title="`rem_question` command help", description="Detailed help on the `rem_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `rem`, `remove` and `remq`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category. Takes 2 arguments, `category` and `question`\nNote: The question must be exactly as it appears.", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}rem_question [ category ] [ question ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    # BLACKLISTING
    @help.command(aliases=['bl'])
    async def blacklist(ctx):
        em = discord.Embed(title="`blacklist` command help", description="Detailed help on the `blacklist` command.")
        em.add_field(name="Aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="Blacklist a role or user. Takes 2 arguments, user/role and application/global", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}blacklist [ @user | user_id | @role | role_id] < application >```", inline=False)
        em.set_footer(text="[ ] - Required argument ;; < > - Optional argument")
        await ctx.send(embed=em)

    @help.command(aliases=['wl'])
    async def whitelist(ctx):
        em = discord.Embed(title="`whitelist` command help", description="Detailed help on the `whitelist` command.")
        em.add_field(name="Aliases", value="This command has one alias: `wl`", inline=False)
        em.add_field(name="Usage", value="Whitelist a role or user. Takes 2 arguments, user/role and application/global", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}whitelist [ @user | user_id | @role | role_id] < application >```", inline=False)
        em.set_footer(text="[ ] - Required argument ;; < > - Optional argument")
        await ctx.send(embed=em)

    # REQUIREMENTS MANAGEMENT
    @help.command(aliases=['ar', 'addreq'])
    async def add_req(ctx):
        em = discord.Embed(title="`add_req` command help", description="Detailed help on the `add_req` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `ar` and `addreq`", inline=False)
        em.add_field(name="Usage", value="Add a role requirement to an application/globally. Takes 2 arguments, `role_requirement` and `application`", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}add_req [ @role | role_id ] < application >```", inline=False)
        em.set_footer(text="[ ] - Required argument ;; < > - Optional argument")
        await ctx.send(embed=em)

    @help.command(aliases=['rr', 'remreq'])
    async def remove_req(ctx):
        em = discord.Embed(title="`remove_req` command help", description="Detailed help on the `remove_req` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `rr` and `remreq`", inline=False)
        em.add_field(name="Usage", value="Remove a role requirement from an application/globally. Takes 2 arguments, `role_requirement` and `application`", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}rem_req [ @role | role_id ] < application >```", inline=False)
        em.set_footer(text="[ ] - Required argument ;; < > - Optional argument")
        await ctx.send(embed=em)

    # OWNERS MANAGEMENT
    @help.command(aliases=['ao'])
    async def add_owner(ctx):
        em = discord.Embed(title="`add_owner` command help", description="Detailed help on the `add_owner` command.")
        em.add_field(name="Aliases", value="This command has one alias: `ao`", inline=False)
        em.add_field(name="Usage", value="Give a user access to all bot admin commands. Takes a single argument, `user`", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}add_req [ @user | user_id ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    @help.command(aliases=['ro'])
    async def rem_owner(ctx):
        em = discord.Embed(title="`rem_owner` command help", description="Detailed help on the `rem_owner` command.")
        em.add_field(name="Aliases", value="This command has one alias: `ro`", inline=False)
        em.add_field(name="Usage", value="Removes a user's access from all bot admin commands. Takes a single argument, `user`", inline=False)
        em.add_field(name="Example Usage", value=f"```{get_prefix()}add_req [ @user | user_id ]```", inline=False)
        em.set_footer(text="[ ] - Required argument")
        await ctx.send(embed=em)

    # APPLLICATION COMMANDS
    @help.command()
    async def accept(ctx):
        em = discord.Embed(title="`accept` command help", description="Detailed help on the `accept` command.")
        em.add_field(name="aliases", value="This command has no aliases.", inline=False)
        em.add_field(name="Usage", value="Accept a user's application.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            ```
    1. {get_prefix()}accept tmod @user be active
    2. {get_prefix()}accept owner user_id```
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['deny', 'decline'])
    async def reject(ctx):
        em = discord.Embed(title="`reject` command help", description="Detailed help on the `reject` command.")
        em.add_field(name="aliases", value="This command has two aliases: `deny`, `decline`", inline=False)
        em.add_field(name="Usage", value="Reject a user's application", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            ```
    1. {get_prefix()}reject tmod @user be active
    2. {get_prefix()}deny owner user_id``` 
            """, inline=False)
        await ctx.send(embed=em)
    @help.command()
    async def consider(ctx):
        em = discord.Embed(title="`consider` command help", description="Detailed help on the `consider` command.")
        em.add_field(name="aliases", value="This command has no aliases.", inline=False)
        em.add_field(name="Usage", value="Consider a user's application", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a three arguments, first, application, then the user (by mention or id) and the third, which is optional, a message:
            ```
    1. {get_prefix()}consider tmod @user I might accept you if you are active more
    2. {get_prefix()}consider gaw_man user_id donate more perhaps```
            """, inline=False)
        await ctx.send(embed=em)

    # DUMP COMMANDS
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
    @help.command(aliases=['dumpb', 'blacklists', 'blacklisted'])
    async def dump_blacklists(ctx):
        em = discord.Embed(title="`dump_blacklist` command help", description="Detailed help on the `dump_questionsblacklistmand.")
        em.add_field(name="aliases", value="This command has three aliases: `dumpb`, `blacklisted`, and `blacklists`", inline=False)
        em.add_field(name="Usage", value="Returns blacklisted users or roles.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, user or role, which is optional:
            ```
    1. {get_prefix()}blacklists usr
    2. {get_prefix()}dumpb 

            Note: The second one will result in all the blacklists stored, being sent.
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

    @help.command(aliases=['re', 'raise'])
    async def raise_er(ctx):
        em = discord.Embed(title="`raise_er` command help", description="Detailed help on the `raise_er` command.")
        em.add_field(name="aliases", value="This command has two aliases: `re` and `raise`.", inline=False)
        em.add_field(name="Usage", value="raise an error", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command a single optional argument:
            1. {get_prefix()}raise It did not reply to me mf
            2. {get_prefix()}re
            """, inline=False)
        await ctx.send(embed=em)
help_cmd()

##########################################################################
############################## get functions #############################
##########################################################################
def get_id_from_mention(mention):
    try:
        mention = str(mention)
        return int(''.join(x for x in mention if x.isdigit()))
    except:
        pass

def get_last_channel():
    with open(r"config\lastch.txt") as file:
        return get_id_from_mention(file.read()) 

def get_app_log_channel():
    with open(r"config\app_log.txt") as file:
        return int(file.read())

def getguild():
    with open(r"config\guild.txt") as file:
        return int(file.read())

async def getusr(id):
    usr = bot.get_user(id)
    if usr is not None:
        pass
    else:
        try:
            usr = await bot.fetch_user(id)
            pass
        except NotFound:
            return False
    return usr


async def getrl(id):
    id = int(id)
    guild = bot.get_guild(getguild())
    role = guild.get_role(id)
    return role

async def write_last_channel(id):
    with open(r"config\lastch.txt", "w") as file:
        file.write(str(id))


async def dumpbls(li, role_or_user):
    if role_or_user == "Role":
        x = "Role"
    elif role_or_user == "User":
        x = "User"
    
    if li == []:
        return("None")
    stl = []
    for i in li:
        try:
            rlname = await getrl(get_id_from_mention((i.split('_')[-1])))
        except:
            rlname = await getusr(get_id_from_mention((i.split('_')[-1])))
        if "gbl" not in i:
            stl.append(f"{x} {rlname.name} cannot apply for application: {i.split('_')[0]}")
        else:
            stl.append(f"{x} {rlname.name} cannot apply to any application")

    tosend = '\n'.join([str(elem) for elem in stl])

    return tosend


def get_questions_from_cat(cat):
    if not os.path.exists(fr'questions\{cat}.txt'):
        open(fr"questions\{cat}.txt", "w")
    with open(fr"questions\{cat}.txt") as file:
        return file.readlines()


def write_answer(usr, app, ques, ans):
    with open(fr"answers\{usr}_{app}.txt", "a") as file:
        file.write(f"{ques}_-_{ans}")

def get_ques(s):
    return (s.split("_-_"))[0]

def get_ans(s):
    return (s.split("_-_"))[1]

def build_ans_embed(usr, app):
    with open(fr"answers\{usr}_{app}.txt") as file:
        x = file.readlines()
        em1 = discord.Embed(title="App Page 1", description=f"Page 1 of application of user: {usr.name} with id {usr.id} applying for {app}")
        em2 = discord.Embed(title="App Page 2", description=f"Page 2 of application of user: {usr.name} with id {usr.id} applying for {app}")
        em3 = discord.Embed(title="App Page 2", description=f"Page 2 of application of user: {usr.name} with id {usr.id} applying for {app}")
        em4 = discord.Embed(title="App Page 2", description=f"Page 2 of application of user: {usr.name} with id {usr.id} applying for {app}")
        
        for i in range(len(x)):
            if i < 25 or i == 25:
                em1.add_field(name=f"{get_ques(x[i])}", value=f"{get_ans(x[i])}")
            elif i > 25 and (i < 50 or i == 50):
                em2.add_field(name=f"{get_ques(x[i])}", value=f"{get_ans(x[i])}")
            elif i > 50 and (i < 75 or i == 75):
                em3.add_field(name=f"{get_ques(x[i])}", value=f"{get_ans(x[i])}")
            elif i > 75 and (i < 100 or i == 100):
                em4.add_field(name=f"{get_ques(x[i])}", value=f"{get_ans(x[i])}")
    asas = []
    if len(em1.fields) != 0:
        asas.append(em1)
    if len(em2.fields) != 0:
        asas.append(em2)
    if len(em3.fields) != 0:
        asas.append(em3)
    if len(em4.fields) != 0:
        asas.append(em4)

    return asas
##########################################################################
################### Check Depndancy Functions For Less ###################
################### Confoosun in Main Check Functions ####################
##########################################################################


def get_reqs(app):
    some_temp_list = []
    with open(r"config\req.txt") as file:
        for ahi in file.readlines():
            if f"{app}_" in ahi:
                some_temp_list.append(int(ahi.split("_")[-1]))
    return some_temp_list

def get_role_blacklists(app):
    some_temp_list = []
    with open(r"bl\rl_blacklists.txt") as file:
        ah = file.readlines()
        for ahi in ah:
            if f"{app}_" in ahi:
                some_temp_list.append(int(ahi.split("_")[-1]))
    return some_temp_list

def common_member(a, b):
    return(any(i in a for i in b))

def get_role_ids(usrid):
    usr = bot.get_user(usrid)
    roles_ids = []
    for y in usr.roles:
        roles_ids.append(y.id)
    return roles_ids

def checkInFirst(a, b):
    count_a = Counter(a)
    count_b = Counter(b)
  
    for key in count_b:
        if key not in  count_a:
            return False
        if count_b[key] > count_b[key]:
            return False
    return True

def get_active():
    with open(r"config\active_apps.txt") as file:
        return file.readlines()

def emb(title, ques):
    em = discord.Embed(title=title, description=ques)
    em.set_footer("send cancel to cancel your application.")
    return em

def get_hier():
    with open(r"config\hier.txt") as file:
        return file.readlines()
def get_indent(stri):
    return stri.count(" ")

def get_global_user_blacklists():
    stl = []
    with open(r"bl\usr_blacklists.txt") as file:
        for ah in file.readlines():
            if "gbl_" in ah:
                stl.append(ah.split("_")[1])
    return stl

def get_global_role_blacklists():
    stl = []
    with open(r"bl\rl_blacklists.txt") as file:
        for ah in file.readlines():
            if "gbl_" in ah:
                stl.append(ah.split("_")[1])
    return stl

def is_user_blacklisted(app, usrid):
    d = f"{app}_{usrid}"
    with open(r"bl\usr_blacklists.txt") as file:
        return d in file.readlines()

def is_role_blacklisted(usrid, app):
    with open(r"bl\rl_blacklists.txt") as file:
        return common_member((get_role_ids(usrid)), get_role_blacklists(app))

def is_global_usr_bl(id):
    return id in get_global_user_blacklists()

def is_global_role_bl(id):
    return id in get_global_role_blacklists
def is_any_app_active():
    with open(r"config\active_apps.txt") as file:
        if str(file.read()).replace("\n", "") == "":
            return False
        else:
            return True

def is_app_active(app):
    with open(r"config\active_apps.txt") as file:
        if app in file.read():
            return True
    return False

def meets_general_req(usrid):
    return checkInFirst(get_role_ids(usrid), get_reqs("general"))

def can_apply_to_any(usrid):
    x = []
    for app in get_active():
        x.append(checkInFirst(get_role_ids(usrid), get_reqs(app)))
    if True in x:
        return True
    else:
        return False

def meets_app_req(usrid, app):
    return checkInFirst((get_role_ids(usrid)), get_reqs(app))

async def all_checks(ctx, app):
    usrid = ctx.author.id
    if not is_global_usr_bl(usrid):
        if not is_global_role_bl(usrid):
            if is_any_app_active():
                if is_app_active(app):
                    if meets_general_req(usrid):
                        if can_apply_to_any(usrid):
                            if not is_user_blacklisted(app, usrid):
                                if not is_role_blacklisted(usrid, app):
                                    if meets_app_req(usrid, app):
                                        try:
                                            await ctx.author.send("Starting application... hang on a moment...")
                                            return True
                                        except Forbidden:
                                            return("I can't DM you, please make sure your dms are open.")
                                        except HTTPException:
                                            return("An error occured, try again later.")
                                    x = ("You do not meet the requirements to apply to this application")
                                    asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                                    return x
                                x = ("You have a role which is blacklisted from applying for this app")
                                asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                                return x
                            x = ("You are blacklisted from applying for this app.")
                            asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                            return x
                        x =  ("There is no application you can apply to")
                        asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                        return x
                    x = ("You do not meet the general requirements for applying.")
                    asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                    return x
                x = ("This application is not accepting applications at the moment.")
                asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
                return x
            x =  ("There is no applicationg taking responses right now.")
            asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
            return x
        x = ("You have a role which is blacklisted for applying to ANY Application.")
        asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
        return x
    x = ("You are blacklisted for applying to ANY Application. 2bad4u")
    asyncio.create_task(log(f"{ctx.author.id} : {ctx.author} tried to apply, a problem occured: {x}"))
    return x

#################################################
############## Basically all of the #############
############## Actual Bot Commands ##############
################ Only For Admins ################
#################################################

@bot.command(name="set_log_channel", aliases = ["slc", "setlog"])
@commands.is_owner()
async def set_log_channel(ctx, channel: Union[discord.TextChannel]):
    if channel.id == get_reg_log_channel():
        await ctx.send("That is already configured as the regular log channel.")
        return

    try:
        newch = bot.get_channel(channel.id)
        await newch.send(embed=em)
    except:
        await ctx.send(embed=discord.Embed(title="Error!", description="I can't send messages and/or embeds in the specified channel, check permissions, and ping the bot in that channel once.", colour=red))
        return

    with open(r"config/logch.txt", "w") as f:
        f.write(str(channel.id))
    await ctx.send(embed=discord.Embed(title="Task completed successfully!", description=f"Set <#{channel.id}> as regular log channel.", colour=green))
    asyncio.create_task(log(f"Set <#{channel.id}> as regular log channel.", ctx, green))

@bot.command(name="set_app_channel", aliases=["sac", "setapp"])
@commands.is_owner()
async def set_app_channel(ctx, channel: Union[discord.TextChannel]):

    if channel.id == get_app_log_channel():
        await ctx.send("That is already configured as the app log channel.")
        return

    try:
        newch = bot.get_channel(channel.id)
        await newch.send(embed=em)
    except:
        await ctx.send(embed=discord.Embed(title="Error!", description="I can't send messages and/or embeds in the specified channel, check permissions, and ping the bot in that channel once.", colour=red))
        return

    with open(r"config/app_log.txt", "w") as f:
        f.write(str(channel.id))
    await ctx.send(embed=discord.Embed(title="Task completed successfully!", description=f"Set <#{channel.id}> as application log channel.", colour=green))
    asyncio.create_task(log(f"Set <#{channel.id}> as application log channel.", ctx, green))

@bot.command(name="add_question", aliases = ["aq", "add", "addq", "addques"])
@commands.is_owner()
async def add_question(ctx, cat, *, ques):
    x = ques.replace('\n','\\n').replace("\"", "'")
    dsp = x.replace("\\n", " {new_line} ")
    ques = f"{x}\n"
    filename = (fr"questions\{cat}.txt") 

    if ques in get_questions_from_cat(cat):
        await ctx.send(embed=discord.Embed(title="Error!", description=f"`{dsp}`\n is already a question in category `{cat}`", colour=red))
        return

    with open(filename, "a") as file:
        file.write(ques)
    await ctx.send(embed=discord.Embed(title="Task completed successfully!", description=f"Added question `{dsp}` in category `{cat}`", colour=green))
    asyncio.create_task(log(f"Added question \"{dsp}\" in category `{cat}`", ctx, green))

@bot.command(name="rem_question", aliases = ["removeques", "remove", 'rq', "remq"])
@commands.is_owner()
async def rem_question(ctx, cat, *, ques):
    x = ques.replace('\n','\\n')
    dsp = x.replace("\\n", "{new_line}")
    ques = f"{x}\n"
    filename = (fr"questions\{cat}.txt")

    if not os.path.exists(filename):
        await ctx.send(embed=discord.Embed(title="Error!", description=f"`Category: `{cat}` is not present.", colour=red))
        return

    if ques not in get_questions_from_cat(cat):
        await ctx.send(embed=discord.Embed(title="Error!", description=f"`{dsp}`\n is already not a question in category `{cat}`", colour=red))
        return

    with open(filename, "r+") as file:
        file_source = file.read()
        file.seek(0)
        file.truncate()
        file.write(file_source.replace(f"{ques}", ""))

    await ctx.send(embed=discord.Embed(title="Task completed successfully!", description=f"Removed question `{dsp}` from category `{cat}`", colour=green))
    asyncio.create_task(log(f"Removed question \"{dsp}\" from category \"{cat}\"", ctx, red))


@bot.command(name="clear_category", aliases=['cc', 'rc', 'clearcat'])
@commands.is_owner()
async def clear_category(ctx, cat):
    if not os.path.exists(fr'questions\{cat}.txt'):
        await ctx.send(embed=discord.Embed(title="Error!", description=f"Category: `{cat}` does not exist.", colour=red))
        return

    await ctx.send(embed=discord.Embed(title="Confirm Task", description=f"Are you sure you want to delete category `{cat}` and all it's questions?\nReply with `yes` or `no` mate", colour=blue))
    def check(m):
        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
    msg = await bot.wait_for("message", check=check)

    if msg.content != "yes" or msg.content != "y":
        await ctx.send(embed=discord.Embed(title="Task Aborted", description="Aborted removal of category `{cat}`", colour=red))
        return

    os.remove(fr"questions\{cat}.txt")
    await ctx.send(embed=discord.Embed(title="Task completed successfully!", description=f"Removed category `{cat}`", colour=green))
    asyncio.create_task(log(f"Removed category `{cat}`", ctx, red))

@bot.command(name="blacklist", aliases=['bl'])
@commands.is_owner()
async def blacklist(ctx, arg: Union[discord.Member, discord.Role], app=None):
    if arg.id in get_owners():
        await ctx.send("Stop drinking.")
        return

    if isinstance(arg, discord.Member):
        todo = "usr"
    elif isinstance(arg, discord.Role):
        todo = "rl"
    else:
        print("You should not have reached here.")
        return

    if app is not None:
        dets = f"{app}_{arg.id}\n"
        if todo == "usr":
            tosend = f"Blacklisted user `{arg.id} : {arg.name}` for app: `{app}`"
        elif todo == "rl":
            tosend = f"Blacklisted role `{arg.id} : {arg.name}` for app: `{app}`"
    else:
        dets = f"gbl_{arg.id}\n"
        if todo == "usr":
            tosend = f"Blacklisted user `{arg.id} : {arg.name}` globally"
        elif todo == "rl":
            tosend = f"Blacklisted role `{arg.id} : {arg.name}` globally"

    filename = fr"bl\{todo}_blacklists.txt"
    with open(filename) as file:
        if dets in file.readlines():
            await ctx.send(embed=discord.Embed(title="Error!", description="Already Blacklisted.", colour=red))
            return

    with open(filename, "a") as file:
        file.write(dets)

    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=tosend, colour=green))
    asyncio.create_task(tosend, ctx, red)


@bot.command(name="whitelist", aliases=['wl'])
@commands.is_owner()
async def whitelist(ctx, arg: Union[discord.Member, discord.Role], app=None):

    if arg.id in get_owners():
        await ctx.send("Nou.")
        return

    if isinstance(arg, discord.Member):
        todo = "usr"
    elif isinstance(arg, discord.Role):
        todo = "rl"
    else:
        print("You should not have reached here.")
        return

    if app is not None:
        dets = f"{app}_{arg.id}\n"
        if todo == "usr":
            tosend = f"Whitelisted user `{arg.id} : {arg.name}` for app: `{app}`"
        elif todo == "rl":
            tosend = f"Whitelisted role `{arg.id} : {arg.name}` for app: `{app}`"
    else:
        dets = f"gbl_{arg.id}\n"
        if todo == "usr":
            tosend = f"Whitelisted user `{arg.id} : {arg.name}` globally"
        elif todo == "rl":
            tosend = f"Whitelisted role `{arg.id} : {arg.name}` globally"

    filename = fr"bl\{todo}_blacklists.txt"

    with open(filename) as file:
        if dets not in file.readlines():
            await ctx.send(embed=discord.Embed(title="Error!", description="Already Whitelisted.", colour=red))
            return

    with open(filename, "r+") as file:
        file_source = file.read()
        file.seek(0)
        file.truncate()
        file.write(file_source.replace(dets, ""))

    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=tosend, colour=green))
    asyncio.create_task(tosend, ctx, red)


@bot.command(name="add_req", aliases=['ar', 'addreq'])
@commands.is_owner()
async def add_req(ctx, req: Union[discord.Role], app=None):

    if req.id not in [i.id for i in await bot.get_guild(id).roles]:
        await ctx.send("What?")
        return

    if app is not None:
        det = f"{app}_{req.id}\n"
        tosend = f"to apply for {app}"
    else:
        det = f"general_{req.id}\n"
        tosend = f"to apply for any application."

    with open(r"config\req.txt") as file:
        if det in file.readlines():
            await ctx.send(embed=discord.Embed(title="Error!", description="Already a requirement.", colour=red))
            return

    with open(r"config\req.txt", "a") as file:
        file.write(det)

    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Users will now require {req.name} {tosend}.", colour=green))
    asyncio.create_task(log(f"Added role requirement of {req.name} {tosend}", ctx, green))

@bot.command(name="remove_req", aliases=['rr', 'remreq']) 
@commands.is_owner()
async def remove_req(ctx, req: Union[discord.Role], app=None):

    if app != None:
        det = f"{app}_{req.id}\n"
        tosend = f"to apply for {app}"
    else:
        det = f"general_{req.id}\n"
        tosend = "to apply to any application."

    with open(r"config\req.txt") as file:
        if det not in file.readlines():
            await ctx.send(embed=discord.Embed(title="Error!", description="This was never a requirement.", colour=red))
            return

    with open(r"config\req.txt", "r+") as file:
        file_source = file.read()
        file.seek(0)
        file.truncate()
        file.write(file_source.replace(f"{det}", ""))
    
    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Users will no longer require {req.name} {tosend}.", colour=green))
    asyncio.create_task(log(f"Removed role requirement of {req.name} {tosend}", ctx, green))

@bot.command(name="add_owner", aliases=['ao', 'addowner'])
@commands.is_owner()
async def add_owner(ctx, usr: Union[discord.Member]):

    if usr.id == 736147895039819797:
        await ctx.send("Nou.")
        return

    with open(r"config\owners.txt") as file:
        if str(usr.id) in file.read():
            await ctx.send("Already an owner")
            return

    bot.owner_ids.append(usr.id)
    with open(r"config\owners.txt", "a") as file:
        file.write(f"{usr.id}\n")
    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Added user {usr.id} : {usr.name} as owner.", colour=green))
    asyncio.create_task(log(f"Added user `{usr.id} : {usr.name}` as owner.", ctx, green))

@bot.command(name="rem_owner", aliases=['ro', 'remowner'])
@commands.is_owner()
async def rem_owner(ctx, usr: Union[discord.Member]):

    if usr.id == 736147895039819797:
        await ctx.send("Nou.")
        return
    with open(r"config\owners.txt") as file:
        file_source = file.read()
    
        if f"{usr.id}\n" not in file_source:
            await ctx.send("Already not an owner")
            return

    bot.owner_ids.remove(usr.id)
    with open(r"config\owners.txt", "w") as file:
        file.write(file_source.replace(f"{usr.id}\n", ""))

    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Removed user {usr.id} : {usr.name} as owner.", colour=green))
    asyncio.create_task(log(f"Removed user `{usr.id} : {usr.name}` as owner.", ctx, green))


@bot.command(name="consider")
async def consider(ctx, app, usr: Union[discord.Member], *, msg=None):

    if msg != None:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} is being considered. Also, {msg}, colour=blue"))
        asyncio.create_task(log(f"Considered {app} application of user `{usr.id} : {usr.name}`, with message: {msg}", ctx, blue))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Considered {app} application of user `{usr.id} : {usr.name}`,with message: {msg}", colour=blue))
    else:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} is being considered.", colour=blue))
        asyncio.create_task(log(f"Considered {app} application of user `{usr.id} : {usr.name}`.", ctx, blue))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Considered {app} application of user `{usr.id} : {usr.name}`.", colour=blue))

@bot.command(name="accept")
async def accept(ctx, app, usr: Union[discord.Member], *, msg=None):

    if msg != None:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} has been accepted. Also, {msg}, colour=green"))
        asyncio.create_task(log(f"Accepted {app} application of user `{usr.id} : {usr.name}`, with message: {msg}", ctx, green))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Accepted {app} application of user `{usr.id} : {usr.name}`,with message: {msg}", colour=green))
    else:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} has been accepted.", colour=green))
        asyncio.create_task(log(f"Accepted {app} application of user `{usr.id} : {usr.name}`.", ctx, green))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Accepted {app} application of user `{usr.id} : {usr.name}`.", colour=green))

@bot.command(name="reject", aliases=["deny", "decline"])
async def reject(ctx, app, usr: Union[discord.Member], *, msg=None):

    if msg != None:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} has been rejected. Also, {msg}, colour=red"))
        asyncio.create_task(log(f"Rejected {app} application of user `{usr.id} : {usr.name}`, with message: {msg}", ctx, red))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Rejected {app} application of user `{usr.id} : {usr.name}`,with message: {msg}", colour=red))
    else:
        await usr.send(embed=discord.Embed(title="Application status update", description=f"Your application for {app} has been rejected.", colour=red))
        asyncio.create_task(log(f"Rejected {app} application of user `{usr.id} : {usr.name}`.", ctx, red))
        await ctx.send(embed=discord.Embed(title="Application status update", description=f"Rejected {app} application of user `{usr.id} : {usr.name}`.", colour=red))

@bot.command(name="dump_questions", aliases=['questions', 'dumpq'])
@commands.is_owner()
async def dump_questions(ctx, cat=None):
    if cat is not None:
        try:
            with open(fr"questions\{cat}.txt") as file:
                temp = file.read().replace("\\n", " {new_line} ")
                if temp == "":
                    await ctx.send("Empty category")
                else:
                    await ctx.send(embed=discord.Embed(title=f"Questions for category `{cat}`", description=temp))
        except FileExistsError:
            await ctx.send("No such category!")

    else:
        x = next(os.walk("questions"), (None, None, []))[2]
        stl = []
        for i in x:
            stl.append(i.replace(".txt", ""))
        await ctx.send(embed=discord.Embed(title="Categories", description=', '.join([str(elem) for elem in stl]), colour=blue))
        for fl in x:
            with open(fr"questions\{fl}") as file:
                t = file.read()
                if t != "":
                    t = t.replace("\\n", " {new_line} ")
                    emb = discord.Embed(title=f"Questions for the category `{fl.replace('.txt', '')}`", description=t, colour=green)
                else:
                    emb = discord.Embed(title=f"Questions for the category {fl.replace('.txt', '')}", description="No questions, empty category", colour=red)
                await ctx.send(embed=emb)


@bot.command(name="dump_blacklists", aliases=['blacklists', 'blacklisted'])
async def dump_blacklists(ctx, role_or_user=None):

    with open(r"bl\rl_blacklists.txt") as file:
        ab = file.readlines()
        if ab == []:
            return
        st = [ah.replace("\\n", " {new_line} ") for ah in ab]

    with open(r"bl\usr_blacklists.txt") as file:
        ab = file.readlines()
        if ab == []:
            return
        xy = [ah.replace("\\n", " {new_line} ") for ah in ab]

    role_blacklists = await dumpbls(st, "Role")
    user_blacklists = await dumpbls(xy, "User")
    # Add support for more blacklists, more embeds basically
    roleemb = discord.Embed(title="Role blacklists", description=role_blacklists, colour=random.choice([green, red, blue]))
    useremb = discord.Embed(title="User Blacklists", description=user_blacklists, colour=random.choice([green, red, blue]))
    if role_or_user == "role" or role_or_user == "rl":
        await ctx.send(embed=roleemb)

    elif role_or_user == "user" or role_or_user == "usr":
        await ctx.send(embed=useremb)


    elif role_or_user is None:
        await ctx.send(embed=useremb)
        await ctx.send(embed=roleemb)

    else:
        await ctx.send("Only two options you have, `role` or `user`")

@bot.command(name="dump_owners", aliases=['owners',])
async def dump_owners(ctx):
    stl = []
    x = get_owners()
    for i in range(len(x)):
        y = await getusr(x[i])
        stl.append(f"{i+1}. {x[i]} : {y.name}")
    await ctx.send(embed=discord.Embed(title="Owners", description='\n'.join([str(elem) for elem in stl]), colour=0x02dcff))

@bot.command(name="dump_req", aliases=['requirements', 'reqs'])
@commands.is_owner()
async def dump_req(ctx, cat=None):

    if cat == "general":
        await ctx.send(embed=discord.Embed(title="General Requirements", description=get_reqs("general")))

    elif cat is not None and cat != "general":
        await ctx.send(embed=discord.Embed(title=f"Requirements for {cat}", description=get_reqs(cat)))

    elif cat is None:

        with open(f"config\req.txt") as file:
            await ctx.send(embed=discord.Embed(title="All Requirements", description=file.read()))

@bot.command(name="set_prefix", aliases=['sp', 'prefix']) 
@commands.is_owner()
async def set_prefix(ctx, new_prefix):
    bot.command_prefix = new_prefix
    with open(r"config\prefix.txt", "w") as file:
        file.write(new_prefix)
    await ctx.send(embed=discord.embed(title="Prefix change", description=f"Changed the prefix to {new_prefix}", colour=blue))
    asyncio.create_task(log(f"Changed the prefix to {new_prefix}", ctx, blue))


@bot.command(nam="toggle")
@commands.is_owner()
async def toggle(ctx, on_or_off, app):
    rawapp = app
    app = f"{app}\n"
    with open(r"config\active_apps.txt") as file:
        ttt = file.readlines()
        if on_or_off == "on" and app in ttt:
            await ctx.send(embed=discord.Embed(title="Error!", description="Already an active application.", colour=red))
            return
        if on_or_off == "off" and app not in ttt:
            await ctx.send(embed=discord.Embed(title="Error!", description="Already not an active application.", colour=red))
            return
        
        if on_or_off == "on" and app not in ttt:
            with open(r"config\active_apps.txt", "a") as f:
                f.write(app)
            await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Toggled app: `{rawapp}` to `ON`", colour=green))
            await asyncio.create_task(log(f"Toggled app: `{rawapp}` to `ON`", ctx, green))
            return
        if on_or_off == "off" and app in ttt:
            with open(r"config\active_apps.txt", "r+") as file2:
                file_source = file2.read()
                file2.seek(0)
                file2.truncate()
                file2.write(file_source.replace(rawapp, ""))
            await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Toggled app: `{rawapp}` to `OFF`", colour=green))
            await asyncio.create_task(log(f"Toggled app: `{rawapp}` to `OFF`", ctx, green))
            return


@bot.command(name="write_hier", aliases=['wh', 'hier'])
@commands.is_owner()
async def write_hier(ctx, *, hierarchy):
    if hierarchy.replace("`", "") == "" or hierarchy.replace("`", "") == "\n":
        await ctx.send(embed=discord.Embed(title="Error!", description="Can't keep empty hierarchy.", colour=red))
        return
    x = hierarchy.replace('`', "")

    with open(r"config\hier.txt") as file:
        if x in file.read():
            await ctx.send(embed=discord.Embed(title="Error!", description="It's already that", colour=red))
            return


    with open(r"config/hier.txt", "w") as file:
        file.write(x)
    await ctx.send(embed=discord.Embed(title="Task completed successfully", description=f"Set new hierarchy as\n ```{x}```", colour=blue))
    asyncio.create_task(log(f"Set new hierarchy: ```{x}```", ctx, blue))

@bot.listen('on_message')
async def is_mentioned(msg):
    if msg.content == f"<@843774061867827220>" or msg.content == f"<@!843774061867827220>":
        await msg.channel.send(f"Current prefix is: `{get_prefix()}`")

##########################################################################
################################## Error ##################################
################################# Handling ################################
##########################################################################


@set_log_channel.error
@set_app_channel.error
@add_question.error
@rem_question.error
@clear_category.error
@whitelist.error
@blacklist.error
@add_req.error
@remove_req.error
@add_owner.error
@rem_owner.error
@consider.error
@accept.error
@reject.error
@dump_questions
@dump_blacklists
@dump_owners
@dump_req
@set_prefix
@toggle
@write_hier
async def set_log_channel(ctx, error):
    await ctx.invoke(bot.get_command(f"help {ctx.command.name}"))
 

#################################################
############## Basically all of the #############
############## Actual Bot Commands ##############
################# For Public Pog ################
#################################################
@bot.command(name="raise_er", aliases=["re", "raise", "error"])
async def raise_er(ctx, *, context=None):
    try:
        usrid = 736147895039819797
        me = await getusr(usrid)
        if me is not False:
            pass
        else:
            return

        msg = await ctx.send("The author of the bot has been notified of the error raised.")
        await me.send(f"User <@`{ctx.author.id}`> raised error in server `{ctx.message.guild}` with context: {context}\nAnd {msg.jump_url}")
    except Exception as e:
        await me.send(f"{msg.jump_url}\n{e}")

@bot.command(name="apply")
async def apply(ctx, app):
    x = await all_checks(ctx, app)

    if x != True:
        await ctx.reply(x)
    else:
        await ctx.send("Started application in DMs!")
        z = get_hier()

        for i in range(len(z)):
            if i != (len(z)-1):
                if i < (len(z)-1) and get_indent(z[i]) != get_indent(z[i+1]):
                    x = get_hier()[z[i]].replace(':', '\'\'').replace(" ", "")
                    with open(f"questions/{x}.txt") as file:
                        for ques in file.readlines():
                            await ctx.author.send(emb(x, ques))
                            def check(m):
                                return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                            msg = await bot.wait_for("message", check=check)
                            if msg.content != "cancel":
                                write_answer(ctx.author.id, app, ques, msg.content)
                            else:
                                await ctx.author.send("Cancelled application.")
                                log(f"User {ctx.author} cancelled their application.")
                                return

                elif i < (len(z)-1) and get_indent(z[i]) == get_indent(z[i+1]):
                    a1 = str(z[i]).replace(":", "").repalce(" ", "")
                    a2 = str(z[i+1]).replace(":", "").repalce(" ", "")
                    await ctx.author.send(f"Would you like to answer questions for category: {a1} or for category: {a2}\nAnswer with the category name exactly as it appears.")
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    msg = await bot.wait_for("message", check=check)
                    if msg.content != "cancel":
                        with open(f"questions/{msg.content}.txt") as file:
                            for ques in file.readlines():
                                await ctx.author.send(emb(x, ques))
                                def check(m):
                                    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                                msg = await bot.wait_for("message", check=check)
                                if msg.content != "cancel":
                                    write_answer(ctx.author.id, app, ques, msg.content)
                                else:
                                    await ctx.author.send("Cancelled application.")
                                    log(f"User {ctx.author} cancelled their application.")
                                    return
            else:
                if get_indent(z[i]) == get_indent(z[i+1]):
                    a1 = str(z[i]).replace(":", "").repalce(" ", "")
                    a2 = str(z[i+1]).replace(":", "").repalce(" ", "")
                    await ctx.author.send(f"Would you like to answer questions for category: {a1} or for category: {a2}\nAnswer with the category name exactly as it appears.")
                    def check(m):
                        return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                    msg = await bot.wait_for("message", check=check)
                    if msg.content != "cancel":
                        with open(f"questions/{msg.content}.txt") as file:
                            for ques in file.readlines():
                                await ctx.author.send(emb(x, ques))
                                def check(m):
                                    return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
                                msg = await bot.wait_for("message", check=check)
                                if msg.content != "cancel":
                                    write_answer(ctx.author.id, app, ques, msg.content)
                                    await ctx.author.send("Applicationg completed")
                                else:
                                    await ctx.author.send("Cancelled application.")
                                    log(f"User {ctx.author} cancelled their application.")
                                    return




        x = build_ans_embed(ctx.author, app)
        alc = bot.get_channel(get_app_log_channel())
        for a in x:
            alc.send(embed=a)


##########################################
######## FORGET ABOUT THIS STUFF #########
##########################################
def restart_bot():
    os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(name="restart")
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting the bot...")
    await asyncio.create_task(write_last_channel(ctx.channel.id))
    await asyncio.create_task(log(f"Restart", ctx))
    restart_bot()

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shutting down...")
    await asyncio.create_task(write_last_channel(ctx.channel.id))
    await asyncio.create_task(log(f"Shut down", ctx))
    await bot.close()

@bot.command(name="version")
async def version(ctx):
    await ctx.send(f"I am on version {get_version()} (counted since i first came to life).")

@bot.command(name="setguild")
async def setguild(ctx, id):
    id = get_id_from_mention(id)
    with open(r"config\guild.txt", "w") as file:
        file.write(str(id))
    await ctx.send("done")

bot.run(token)
