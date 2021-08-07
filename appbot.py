import asyncio, discord, os, sys
from discord.errors import Forbidden, HTTPException, NotFound
from discord.ext import commands
from collections import Counter

from discord.gateway import DiscordClientWebSocketResponse
# from discord.utils import get
em = discord.Embed(title="Test Embed", description="Just ensuring i can send messages and embeds here")

token = sys.argv[1]

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


def get_id_from_mention(mention):
    try:
        mention = str(mention)
        return int(''.join(x for x in mention if x.isdigit()))
    except:
        pass
def get_last_channel():
    with open(r"config\lastch.txt") as file:
        return get_id_from_mention(file.read()) 

bot = commands.Bot(command_prefix=get_prefix(), owner_ids=get_owners())
bot.remove_command('help')
bot.case_insensitive = True


def get_log_channel():
    with open(r"config\logch.txt") as file:
        x = int(file.read())
    return x









async def log(content, ctx=None):
    if ctx is not None:
        dsc_content = discord.Embed(title=content, description=f"{ctx.author.id} | {ctx.author.name}")
        content = f"{ctx.author.id} | {ctx.author.name} | {content}"
    else:
        content = f"{content}\n"
        dsc_content = discord.Embed(title=content, description=f"None")


    try:
        with open(r"config\log.txt", "a") as file:
            file.write(content)
        x = get_log_channel()
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
    ch = await bot.fetch_channel(get_last_channel())
    await ch.send("online")
    await asyncio.create_task(log("Came online"))
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
        em.add_field(name="Usage", value="This command will set the channel where logs will be written. Logs include commands used and status of applications.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the channel argument
            You can give the channel ID, or the channel mention:
            ```
    {get_prefix()}set_log_channel #channel
    {get_prefix()}set_log_channel channel_id```
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['sac', 'setapp'])
    async def set_app_channel(ctx):
        em = discord.Embed(title="`set_app_channel` command help", description="Detailed help on the `set_app_channel` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `sac` and `setapp`", inline=False)
        em.add_field(name="Usage", value="Set the channel where completed applications appear.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the channel argument
            You can give the channel ID, or the channel mention:
            ```
    {get_prefix()}set_app_channel #channel
    {get_prefix()}set_app_channel channel_id```
            """, inline=False)
        await ctx.send(embed=em)

    # QUESTION MANAGEMENT COMMANDS
    @help.command(aliases=['add', 'aq', 'addq'])
    async def add_question(ctx):
        em = discord.Embed(title="`add_question` command help", description="Detailed help on the `add_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `add`, `aq` and `addq`", inline=False)
        em.add_field(name="Usage", value="Adds a question to a category. Makes a category if there is no question in the category before.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, those are, the category argument and the question itself:
            ```
    {get_prefix()}add_question dank What prestige level are you?
    {get_prefix()}addq general How old can you be?```
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['rem', 'remove', 'rq', 'remq'])
    async def rem_question(ctx):
        em = discord.Embed(title="`rem_question` command help", description="Detailed help on the `rem_question` command.")
        em.add_field(name="aliases", value="This command has three aliases: `rem`, `remove` and `remq`", inline=False)
        em.add_field(name="Usage", value="Removes a question from a category. Note: The question must be exactly as it appears.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, those are, the category argument and the question itself:
            ```
    {get_prefix()}rem_question dank What prestige level are you?
    {get_prefix()}rq general How old can you be?```
            """, inline=False)
        await ctx.send(embed=em)

    @help.command(aliases=['bl'])
    async def blacklist(ctx):
        em = discord.Embed(title="`blacklist` command help", description="Detailed help on the `blacklist` command.")
        em.add_field(name="Aliases", value="This command has one alias: `bl`", inline=False)
        em.add_field(name="Usage", value="Blacklist a role or user by id or mention, for a specific application or globally.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the user or role mention or id, and the second, which is optional, the name of the application:
            ```

    {get_prefix()}blacklist @role tmod
    {get_prefix()}blacklist user_id owner
    {get_prefix()}blacklist user_id```

            Note: The last one will result in a global blacklist of the user
            """, inline=False)
        await ctx.send(embed=em)

    # BLACKLISTING
    @help.command(aliases=['wl'])
    async def whitelist(ctx):
        em = discord.Embed(title="`whitelist` command help", description="Detailed help on the `whitelist` command.")
        em.add_field(name="Aliases", value="This command has one alias: `wl`", inline=False)
        em.add_field(name="Usage", value="Whitelist a role or user by id or mention, for a specific application or globally.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the user or role mention or id, and the second, which is optional, the name of the application:
            ```
    {get_prefix()}whitelist @role tmod
    {get_prefix()}whitelist user_id owner
    {get_prefix()}wl user_id```
            
            Note: The last one will result in a global whitelist of the user
            """, inline=False)
        await ctx.send(embed=em)

    # REQUIREMENTS MANAGEMENT
    @help.command(aliases=['ar', 'addreq'])
    async def add_req(ctx):
        em = discord.Embed(title="`add_req` command help", description="Detailed help on the `add_req` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `ar` and `addreq`", inline=False)
        em.add_field(name="Usage", value="Add a role requirement to an application or globally.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the role mention or id, and the second, which is optional, the name of the application:
            ```
    {get_prefix()}add_req @role tmod
    {get_prefix()}add_req role_id owner
    {get_prefix()}ar role_id```
            
            Note: The last one will result in role_id being a requirement for all applicatoins, i.e. a general req
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['rr', 'remreq'])
    async def remove_req(ctx):
        em = discord.Embed(title="`remove_req` command help", description="Detailed help on the `remove_req` command.")
        em.add_field(name="Aliases", value="This command has two aliases: `rr` and `remreq`", inline=False)
        em.add_field(name="Usage", value="Remove a role requirement to an application or globally", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes two arguments, the first, the role mention or id, and the second, which is optional, the name of the application:
            ```
    {get_prefix()}rem_req @role tmod
    {get_prefix()}rem_req role_id owner
    {get_prefix()}rr role_id```

            Note: The third one will result in role_id NO LONGER being a requirement for all applicatoins, i.e. a general req
            """, inline=False)
        await ctx.send(embed=em)

    # OWNERS MANAGEMENT
    @help.command(aliases=['ao'])
    async def add_owner(ctx):
        em = discord.Embed(title="`add_owner` command help", description="Detailed help on the `add_owner` command.")
        em.add_field(name="Aliases", value="This command has one alias: `ao`", inline=False)
        em.add_field(name="Usage", value="Makes a user, the owner of the bot. This user will now be able to access ALL THE admin commands.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the user mention or id:
            ```
    {get_prefix()}add_owner @user
    {get_prefix()}ao user_id```

            Note: Read the usage of this command again. Also requires bot restart to take effect
            """, inline=False)
        await ctx.send(embed=em)
    @help.command(aliases=['ro'])
    async def rem_owner(ctx):
        em = discord.Embed(title="`rem_owner` command help", description="Detailed help on the `rem_owner` command.")
        em.add_field(name="Aliases", value="This command has one alias: `ro`", inline=False)
        em.add_field(name="Usage", value="Removes a user from being a bot's owner.", inline=False)
        em.add_field(name="Syntax", value=f"""
            This command takes a single argument, that is, the user mention or id:
            ```
    {get_prefix()}rem_owner @user
    {get_prefix()}ro user_id```

            Note: Read the usage of this command again. Also requires bot restart to take effect.
            """, inline=False)
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
    async def dump_blacklist(ctx):
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
################### some tiny dependant functions ########################
#################### for good and happy working ##########################
##########################################################################

def get_guild():
    with open(r"config\guild.txt") as file:
        return int(file.read())

async def write_last_channel(id):
    with open(r"config\lastch.txt", "w") as file:
        file.write(str(id))

async def return_name_of_user(id):
    usr = await getusr(id)
    if usr != False:
        return usr.name

async def return_name_of_role(id):
    id = int(id)
    guild = bot.get_guild(get_guild())
    role = guild.get_role(id)
    return role.name


def add_question_func(cat, ques):
    if os.path.exists(fr'questions\{cat}.txt'):
        pass
    else:
        open(fr"questions\{cat}.txt", "w")
        pass

    try:
        with open(fr"questions\{cat}.txt", "a") as file:
            file.write(ques)
            return True
    except Exception as e:
        return False

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

def remove_question(cat, ques):
    try:
        with open(fr"questions\{cat}.txt") as file:
            file_source = file.read()
        with open(fr"questions\{cat}.txt", "w") as file:
            file.write(file_source.replace(f"{ques}", ""))
        return True
    except:
        return False

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
            rlname = await return_name_of_role(get_id_from_mention((i.split('_')[-1])))
        except:
            rlname = await return_name_of_user(get_id_from_mention((i.split('_')[-1])))
        if "gbl" not in i:
            stl.append(f"{x} {rlname} cannot apply for application: {i.split('_')[0]}")
        else:
            stl.append(f"{x} {rlname} cannot apply to any application")

    tosend = '\n'.join([str(elem) for elem in stl])

    return tosend

def write_log_channel(chid):
    with open(r"config/logch.txt", "w") as f:
        f.write(chid)

def write_applog(chid):
    with open(r"config/applog.txt", "w") as f:
        f.write(chid)

def write_whitelist_user(usrid, app=None):
    usrid = get_id_from_mention(usrid)
    if app is not None:
        with open(r"bl\usr_blacklists.txt") as file:
            if f"{app}_{usrid}\n" not in file.readlines():
                return False
            else:
                pass
        with open(r"bl\usr_blacklists.txt") as file:
            file_source = file.read()
        with open(r"bl\usr_blacklists.txt", "w+") as f:
            f.write(file_source.replace(f"{app}_{usrid}\n", ""))
            return True
    else:
        with open(r"bl\usr_blacklists.txt") as file:
            if f"gbl_{usrid}\n" not in file.readlines():
                return False
            else:
                pass
        with open(r"bl\usr_blacklists.txt") as file:
            file_source = file.read()
        with open(r"bl\usr_blacklists.txt", "w+") as f:
            f.write(file_source.replace(f"gbl_{usrid}\n", ""))
            return True

def write_whitelist_role(rlid, app=None):
    rlid = get_id_from_mention(rlid)
    if app is not None:
        with open(r"bl\rl_blacklists.txt") as file:
            if f"{app}_{rlid}" not in file.read():
                return False
            else:
                pass
        with open(r"bl\rl_blacklists.txt") as file:
            file_source = file.read()

        with open(r"bl\rl_blacklists.txt", "w+") as f:
            f.write(file_source.replace(f"{app}_{rlid}\n", ""))
            return True
    else:
        with open(r"bl\rl_blacklists.txt") as file:
            if f"gbl_{rlid}" not in file.read():
                return False
            else:
                pass
        with open(r"bl\rl_blacklists.txt") as file:
            file_source = file.read()

        with open(r"bl\rl_blacklists.txt", "w+") as f:
            f.write(file_source.replace(f"gbl_{rlid}\n", ""))
            return True

def write_blacklist_user(usrid, app=None):
    usrid = get_id_from_mention(usrid)
    if app is not None:
        with open(r"bl\usr_blacklists.txt") as file:
            if f"{app}_{usrid}\n" in file.readlines():
                return False
            else:
                pass
        with open(r"bl\usr_blacklists.txt", "a") as f:
            f.write(f"{app}_{usrid}\n")
            return True
    else:
        with open(r"bl\usr_blacklists.txt") as file:
            if f"gbl_{usrid}\n" in file.readlines():
                return False
            else:
                pass
        with open(r"bl\usr_blacklists.txt", "a") as f:
            f.write(f"gbl_{usrid}\n")
            return True

def write_blacklist_role(rlid, app=None):
    rlid = get_id_from_mention(rlid)
    if app is not None:
        with open(r"bl\rl_blacklists.txt") as file:
            if f"{app}_{rlid}\n" in file.readlines():
                return False
            else:
                pass
        with open(r"bl\rl_blacklists.txt", "a") as f:
            f.write(f"{app}_{rlid}\n")
            return True
    else:
        with open(r"bl\rl_blacklists.txt") as file:
            if f"gbl_{rlid}\n" in file.readlines():
                return False
            else:
                pass

        with open(r"bl\rl_blacklists.txt", "a") as f:
            f.write(f"gbl_{rlid}\n")
            return True

def get_ques_addq(cat):
    if os.path.exists(fr'questions\{cat}.txt'):
        pass
    else:
        open(fr"questions\{cat}.txt", "w")
        pass
    with open(fr"questions\{cat}.txt") as file:
        return file.readlines()

def get_applog():
    with open(r"config\applog.txt") as file:
        return int(file.read())


# def get_app_role(app):
#     with open(r"config\app_role.txt") as file:
#         if app not in file.read():
#             return
#         else:
#             for a in file.readlines():
#                 if app in a:
#                     return (a.split("_"))[-1]

# async def acc_app(ctx, app, usrid):
#     try:
#         usr = await bot.get_user(usrid)
#         rl = get(ctx.guild.roles, id=(int(get_app_role(app))))
#         await usr.add_roles(rl)
#     except:
#         pass

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
        ah = file.readlines()
        for ahi in ah:
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

def get_general_req():
    some_temp_list = []
    with open(r"config\req.txt") as file:
        ah = file.readlines()
        for ahi in ah:
            if "general_" in ahi:
                some_temp_list.append(int(ahi.split("_")[-1]))
    return some_temp_list

def checkInFirst(a, b):
     #getting count
    count_a = Counter(a)
    count_b = Counter(b)
  
    #checking if element exsists in second list
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

##########################################################################
############################# All The Checks #############################
############################ Yeah All of Them ############################
##########################################################################  
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
    return checkInFirst(get_role_ids(usrid), get_general_req())

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
async def set_log_channel(ctx, channel):
    channel = get_id_from_mention(channel)
    if channel == get_log_channel():
        await ctx.send("That is already configured as the log channel.")
        return
    try:
        sa = await bot.fetch_channel(int(channel))
        if isinstance(sa, discord.TextChannel):
            if len(str(channel)) == 18:
                try:
                    await sa.send(embed=em)
                    try:
                        write_log_channel(str(channel))
                        await ctx.send("I configured <#{channel}> to log everything other than applications!")
                        asyncio.create_task(log(f"set {channel} as log channel", ctx))
                    except Exception as e:
                        await ctx.send(e)

                except Exception as e:
                    await ctx.send(e)
                    await ctx.send("I can't send messages and/or embeds in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel/")
            else:
                await ctx.send(f"Channel argument has been improperly passed.")
        else:
            await ctx.reply("Not a valid text channel...")

    except Exception as e:
        await ctx.reply(e)
        return


@bot.command(name="set_app_channel", aliases=["sac", "setapp"])
@commands.is_owner()
async def set_app_channel(ctx, chid):
    channel = get_id_from_mention(chid)
    if channel == get_applog():
        await ctx.send("That is already configured as the applog channel.")
        return
    try:
        sa = await bot.fetch_channel(int(channel))
        if isinstance(sa, discord.TextChannel):
            if len(str(channel)) == 18:
                try:
                    await sa.send(embed=em)
                    try:
                        write_applog(str(channel))
                        await ctx.send("I configured <#{channel}> to log applications!")
                        asyncio.create_task(log(f"set {channel} as log applications", ctx))
                    except Exception as e:
                        await ctx.send(e)

                except Exception as e:
                    await ctx.send(e)
                    await ctx.send("I can't send messages and/or embeds in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel/")
            else:
                await ctx.send(f"Channel argument has been improperly passed.")
        else:
            await ctx.reply("Not a valid text channel...")

    except Exception as e:
        await ctx.reply(e)
        return

@bot.command(name="add_question", aliases = ["aq", "add", "addq"])
@commands.is_owner()
async def add_question(ctx, cat, *, ques):
    x = ques.replace('\n','\\n')
    dsp = x.replace("\\n", "{new_line}")
    ques = f"{x}\n"
    if ques in get_ques_addq(cat):
        await ctx.send("Already a question")
        return
    else:
        try:
            if add_question_func(cat, ques):
                await ctx.send(f"Added question `{dsp}` in category `{cat}`")
                asyncio.create_task(log(f"Added question \"{dsp}\" in category \"{cat}\"", ctx))
            else:
                await ctx.send("Idk some error occured")
        except Exception as e:
            await ctx.send(e)


@bot.command(name="rem_question", aliases = ["rem", "remove", 'rq', "remq"])
@commands.is_owner()
async def rem_question(ctx, cat, *, ques):
    x = ques.replace('\n','\\n')
    dsp = x.replace("\\n", "{new_line}")
    ques = f"{x}\n"
    if ques not in get_ques_addq(cat):
        await ctx.send("Already not a question")
        return
    try:
        if remove_question(cat, ques):
            await ctx.send(f"Removed question `{dsp}` in category `{cat}`")
            asyncio.create_task(log(f"Removed question \"{dsp}\" from category \"{cat}\"", ctx))
        else:
            await ctx.send("idk some error came oof.")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="whitelist", aliases=['wl'])
@commands.is_owner()
async def whitelist(ctx, id, app=None):
    id = get_id_from_mention(id)
    if id == 736147895039819797:
        await ctx.send("Nou.")
        return
    else:
        pass
    try:
        await bot.fetch_user(id)
        pass    
    except NotFound:
        try:
            if write_whitelist_role(id, app):
                if app is not None:
                    await ctx.send(f"Whitelist role {id} : {await return_name_of_role(id)} for app {app}")
                    asyncio.create_task(log(f"Whitelisted role {id} : {await return_name_of_role(id)} for app {app}", ctx))
                else:
                    await ctx.send(f"Whitelist role {id} : {await return_name_of_role(id)} globally")
                    asyncio.create_task(log(f"Whitelisted role {id} : {await return_name_of_role(id)} globally", ctx))

            else:
                await ctx.send("Already Whitelisted")
        except HTTPException:
            await ctx.send("Error, could you please re-run the command")
        return
    if write_whitelist_user(id, app):
        if app is not None:
            await ctx.send(f"Whitelisted user {id} : {await return_name_of_user(id)} for app {app}")
            asyncio.create_task(log(f"Whitelisted user {id} : {await return_name_of_user(id)} for app {app}", ctx))
        else:
            await ctx.send(f"Whitelisted user {id} : {await return_name_of_user(id)} globally")
            asyncio.create_task(log(f"Whitelisted user {id} : {await return_name_of_user(id)} globally", ctx))
    else:
        await ctx.send("Already whitelisted?")

@bot.command(name="blacklist", aliases=['bl'])
@commands.is_owner()
async def blacklist(ctx, id, app=None):
    id = get_id_from_mention(id)
    if id == 736147895039819797:
        await ctx.send("Nou.")
        return
    else:
        pass
    try:
        await bot.fetch_user(id)
        pass
    except NotFound:
        try:
            if write_blacklist_role(id, app):
                if app is not None:
                    await ctx.send(f"Blacklisted role `{id} : {await return_name_of_role(id)}` for app `{app}`")
                    asyncio.create_task(log(f"Blacklisted role `{id} : {await return_name_of_role(id)}` for app `{app}`", ctx))
                else:
                    await ctx.send(f"Blacklisted role `{id} : {await return_name_of_role(id)}` globally.")
                    asyncio.create_task(log(f"Blacklisted role `{id} : {await return_name_of_role(id)}` globally", ctx))

            else:

                await ctx.send("Already Blacklisted")
            return
        except HTTPException:
            await ctx.send("Error, could you please re-run the command")
            return
    if write_blacklist_user(id, app):
        if app is not None:
            await ctx.send(f"Blacklisted user `{id} : {await return_name_of_user(id)}` for app `{app}`")
            asyncio.create_task(log(f"Blacklisted user `{id} : {await return_name_of_user(id)}` for app `{app}`", ctx))
        else:
            await ctx.send(f"Blacklisted user `{id} : {await return_name_of_user(id)}` globally")
            asyncio.create_task(log(f"Blacklisted user `{id} : {await return_name_of_user(id)}` globally", ctx))
    else:
        await ctx.send("Already Blacklisted")

@bot.command(name="add_req", aliases=['ar', 'addreq'])
@commands.is_owner()
async def add_req(ctx, req, app=None):
    req = get_id_from_mention(req)
    try:
        guild = bot.get_guild(get_guild())
        guild.get_role(req)
        pass
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
        return
    except NotFound:
        await ctx.send("I am taking only roles as requirements as of now.")
        return

    if app != None:
        det = f"{app}_{req}\n"
        ad = f"to apply for {app}"
    else:
        det = f"general_{req}\n"
        ad = "to apply to any application."

    with open(r"config\req.txt") as file:
        if det in (file.readlines()):
            await ctx.send("This is already a requirement.")
            return
        else:
            with open(r"config\req.txt", "a") as file:
                file.write(det)
            await ctx.send(f"Users will now require {await return_name_of_role(req)} {ad}.")
            asyncio.create_task(log(f"Added role requirement of {await return_name_of_role(req)} {ad}", ctx))


@bot.command(name="remove_req", aliases=['rr', 'remreq']) 
@commands.is_owner()
async def remove_req(ctx, req, app=None):
    req = get_id_from_mention(req)
    try:
        guild = bot.get_guild(get_guild())
        guild.get_role(req)
        pass
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
        return
    except NotFound:
        await ctx.send("I am taking only roles as requirements as of now.")
        return

    if app != None:
        det = f"{app}_{req}\n"
        ad = f"to apply for {app}"
    else:
        det = f"general_{req}\n"
        ad = "to apply to any application."

    with open(r"config\req.txt") as file:
        if det not in (file.readlines()):
            await ctx.send("This was never a requirement.")
            return
        else:
            with open(r"config\req.txt") as f:
                file_source = f.read()
            with open(r"config\req.txt", "w") as f:
                f.write(file_source.replace(f"{det}", ""))
            await ctx.send(f"Users will no longer require {await return_name_of_role(req)} {ad}.")
            asyncio.create_task(log(f"Removed role requirement of {await return_name_of_role(req)} {ad}", ctx))

@bot.command(name="add_owner", aliases=['ao'])
@commands.is_owner()
async def add_owner(ctx, id):
    id = get_id_from_mention(id)
    if id == 736147895039819797:
        await ctx.send("Nou.")
        return
    try:
        await bot.fetch_user(id)
        pass
    except NotFound:
        await ctx.send("Not a user")
        return
    
    with open(r"config\owners.txt") as file:
        if str(id) in file.read():
            await ctx.send("Already an owner")
            return
        else:
            pass
    with open(r"config\owners.txt", "a") as file:
            file.write(f"{str(id)}\n")
            await ctx.send(f"Added user {id} : {await return_name_of_user(id)} as owner. Restart required.")
            asyncio.create_task(log(f"Added user {id} : {await return_name_of_user(id)} as owner.", ctx))

@bot.command(name="rem_owner", aliases=['ro'])
@commands.is_owner()
async def rem_owner(ctx, id):
    id = get_id_from_mention(id)
    if id == 736147895039819797:
        await ctx.send("Nou.")
        return

    try:
        await bot.fetch_user(id)
        pass
    except NotFound:
        await ctx.send("Not a user")
        return

    try:
        with open(r"config\owners.txt") as file:
            file_source = file.read()
            if f"{id}\n" in file_source:
                pass
            else:
                await ctx.send("Already not an owner")
                return
        with open(r"config\owners.txt", "w") as file:
            file.write(file_source.replace(f"{id}\n", ""))
        await ctx.send(f"Removed user {id} : {await return_name_of_user(id)} from owner. Restart required.")
        asyncio.create_task(log(f"Removed user {id} : {await return_name_of_user(id)} from owner.", ctx))

    except Exception as e:
        await ctx.send(e)

@bot.command(name="clear_category", aliases=['cc', 'rc', 'clearcat'])
async def clear_category(ctx, cat):
    if os.path.exists(fr'questions\{cat}.txt'):
        await ctx.send(f"Are you sure you want to delete category `{cat}` and all it's questions?\nYes or no mate")
        def check(m):
            return m.author.id == ctx.author.id and m.channel.id == ctx.channel.id
        msg = await bot.wait_for("message", check=check)
        if msg.content == "yes" or msg.content == "y":
            pass
        else:
            await ctx.send("Fine then, I won't.")
            return
    else:
        await ctx.send("No such category.")
        return

    os.remove(fr"questions\{cat}.txt")
    asyncio.create_task(log(f"Removed category {cat}", ctx))
    await ctx.send(f"Removed category `{cat}`")



@bot.command(name="consider")
async def consider(ctx, app, usrid, *, msg=None):
    usrid = get_id_from_mention(usrid)
    usr = await getusr(usrid)
    if usr is not False:
        pass
    else:
        return

    if msg != None:
        await usr.send(f"Your application for {app} is being considered. Also, {msg}")
        asyncio.create_task(log(f"Considered {usrid}'s application for {app}, with message: {msg}", ctx))
        await ctx.send(f"Considered {usrid}'s application for {app}, with message: {msg}")
    else:
        await usr.send(f"Your application for {app} is being considered.")
        asyncio.create_task(log(f"Considered {usrid}'s application for {app}.", ctx))
        await ctx.send(f"Considered {usrid}'s application for {app}.")

@bot.command(name="accept")
async def accept(ctx, app, usrid, *, msg=None):
    usrid = get_id_from_mention(usrid)
    usr = await getusr(usrid)
    if usr is not False:
        pass
    else:
        return

    if msg != None:
        await usr.send(f"Your application for {app} has been accepted. Also, {msg}")
        asyncio.create_task(log(f"Accepted {usrid}'s application for {app}, with message: {msg}", ctx))
        await ctx.send(f"Accepted {usrid}'s application for {app}, with message: {msg}")
    else:
        await usr.send(f"Your application for {app} has been accepted.")
        asyncio.create_task(log(f"Accepted {usrid}'s application for {app}.", ctx))
        await ctx.send(f"Accepted {usrid}'s application for {app}.")
    # try:
    #     await acc_app(ctx, app, usrid)
    #     await ctx.send("Added role to user")
    # except Exception as e:
    #     await ctx.send(f"error: {e}")

@bot.command(name="reject", aliases=["deny", "decline"])
async def reject(ctx, app, usrid, *, msg=None):
    usrid = get_id_from_mention(usrid)
    usr = await getusr(usrid)
    if usr is not False:
        pass
    else:
        return

    if msg != None:
        await usr.send(f"Your application for {app} has been rejected. Also, {msg}")
        asyncio.create_task(log(f"Rejected {usrid}'s application for {app}, with message: {msg}", ctx))
        await ctx.send(f"Rejected {usrid}'s application for {app}, with message: {msg}")
    else:
        await usr.send(f"Your application for {app} has been rejected.")
        asyncio.create_task(log(f"Rejected {usrid}'s application for {app}.", ctx))
        await ctx.send(f"Rejected {usrid}'s application for {app}.")

@bot.command(name="dump_questions", aliases=['dump', 'questions', 'dumpq'])
@commands.is_owner()
async def dump_questions(ctx, cat=None):
    if cat != None:
        try:
            with open(fr"questions\{cat}.txt") as file:
                temp = file.read().replace("\\n", " {new_line} ")
                if temp == "":
                    temp = "No questions, empty category"
                await ctx.send(f"""
                ```ini
[ Questions for "{cat}" category]

{temp}```""")
        except FileExistsError:
            await ctx.send("No such category!")
        except Exception as e:
            await ctx.send(e)
    else:
        x = next(os.walk("questions"), (None, None, []))[2]
        xy = str(x).replace(".txt", "")
        await ctx.send(f"""
        ```ini
[ Categories ]

{xy}```""")
        for fl in x:
            with open(fr"questions\{fl}") as file:
                t = file.read()
                if t != "":
                    t = t.replace("\\n", " {new_line} ")
                    emb = discord.Embed(title=f"Questions for the category `{fl.replace('.txt', '')}`", description=t)
                else:
                    emb = discord.Embed(title=f"Questions for the category {fl.replace('.txt', '')}", description="No questions, empty category")
                await ctx.send(embed=emb)

# here i am




@bot.command(name="dump_blacklist", aliases=['dumpb', 'blacklists', 'blacklisted'])
async def dump_blacklist(ctx, role_or_user=None):
    with open(r"bl\rl_blacklists.txt") as file:
        x = file.readlines()
        if str(x) != []:
            pass
        else:
            return
        
        st = []
        for ah in x:
            st.append(ah.replace("\\n", " {new_line} "))
    with open(r"bl\usr_blacklists.txt") as file:
        ab = file.readlines()
        if str(ab) != []:
            pass
        else:
            return
        
        xy = []
        for ah in ab:
            xy.append(ah.replace("\\n", " {new_line} "))

    role_blacklists = await dumpbls(st, "Role")
    user_blacklists = await dumpbls(xy, "User")
    # Add support for more blacklists, more mebeds basically

    if role_or_user == "role" or role_or_user == "rl":
        emb = discord.Embed(title="Blacklists", description=" Role Blacklists\n‎")
        emb.add_field(name="Role Blacklists", value=f"{role_blacklists}\n", inline=False)
        await ctx.send(embed=emb)

    elif role_or_user == "user" or role_or_user == "usr":
        emb = discord.Embed(title="Blacklists", description="User Blacklists\n‎", colour=0x02dcff)
        emb.add_field(name="User Blacklists", value=f"{user_blacklists}\n", inline=False)
        await ctx.send(embed=emb)


    elif role_or_user is None:
        emb = discord.Embed(title="Blacklists", description="User and Role Blacklists\n‎")
        emb.add_field(name="User Blacklists", value=f"{user_blacklists}\n‎", inline=False)
        emb.add_field(name="Role Blacklists", value=role_blacklists, inline=False)
        await ctx.send(embed=emb)

    else:
        await ctx.send("Error")

@bot.command(name="dump_owners", aliases=['owners', 'do'])
async def dump_owners(ctx):
    await ctx.send(get_owners())


@bot.command(name="dump_req", aliases=['dumpr', 'requirements', 'reqs'])
@commands.is_owner()
async def dump_req(ctx, cat=None):
    if cat == "general":
        await ctx.send(f"""`
        ``ini
[ General Requirements ]

{get_general_req()}```""")
    elif cat is not None and cat != "general":
        await ctx.send(f"""
        ```ini
[ {cat} Requirements ]

{get_reqs(cat)}```""")
    elif cat is None:
        await ctx.send(f"""
        ```ini
[ General Requiements ]

{get_general_req()}

[ {cat} Requirements ]

{get_reqs(cat)}```""")

# Still working on them

@bot.command(name="embed_colour", aliases=["emc", "ec", "colour", "embc"])
async def embed_colour(ctx, embed_type=None):
    if embed_type is None:
        await ctx.send("""
You need to give the name of the embed for which you want to change the colour of. Currently, you can set it for:
1) dump_question_embed
2) dump_req_embed
3) dump_bl_embed
4) confirmation_embed (confirmation or success same thing)
5) fail_embed
""")



# here me i is
@bot.command(name="set_prefix", aliases=['sp']) 
@commands.is_owner()
async def set_prefix(ctx, new_prefix):
    with open(r"config\prefix.txt", "w") as file:
        file.write(new_prefix)

@bot.command(nam="toggle")
@commands.is_owner()
async def toggle(ctx, on_or_off, app):
    details = f"{app}"
    with open(r"config\active_apps.txt", "a+") as file:
        x = file.readlines()
        if on_or_off == "on":
            if details in str(x):
                return
            else:
                file.write(f"\n{details}")
        elif on_or_off == "off":
            if details not in str(x):
                return
            else:
                with open(r"config\active_apps", "r+") as file2:
                    file_source = file2.read()
                    file2.write(file_source.replace(f"{details}", ""))


@bot.command(name="write_hier", aliases=['wh'])
@commands.is_owner()
async def write_hier(ctx):
    if str(ctx.message).replace("`", "") != "" or str(ctx.message).replace("`", "") != "\n":
        with open(r"config/hier.txt", "w") as file:
            file.write(str(ctx.message).replace('`', ""))
@bot.listen('on_message')
async def is_mentioned(msg):
    if msg.content == f"<@843774061867827220>" or msg.content == f"<@!843774061867827220>":
        await msg.channel.send(f"ME PREFIX IS `{get_prefix()}` YEY")

##########################################################################
################################## Error ##################################
################################# Handling ################################
##########################################################################

@set_app_channel.error
async def set_app_channel(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Channel argument where?\nIt\'s configured as <#{get_applog()}> rn btw')

@set_log_channel.error
async def set_log_channel(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f'Channel argument where?\nIt\'s configured as <#{get_log_channel()}> rn btw')

@add_question.error
async def add_question(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}add_question category how dumb can a person be?`")

@rem_question.error
async def rem_question(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}rem_question category how dumb can a person be?`")

@whitelist.error
async def whitelist(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen.. this is how you use this command: `{get_prefix()}whitelist @user owner`")

@blacklist.error
async def blacklist(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen.. this is how you use this command: `{get_prefix()}blacklist @user owner`")

@add_req.error
async def add_req(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}add_req @role owner`")

@remove_req.error
async def add_req(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}remove_req @role owner`")

@add_owner.error
async def add_owner(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}add_owner @user`")

@rem_owner.error
async def rem_owner(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}rem_owner @user`")

@consider.error
async def consider(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}consider tmod @user be more active`")

@accept.error
async def accept(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}accept tmod @user fast demotes")

@reject.error
async def reject(ctx, error):
    if isinstance(error, commands.CommandInvokeError):
        error = error.original

    if isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(f"Listen... this is how you use this command: `{get_prefix()}reject tmod @user`")

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
        alc = bot.get_channel(get_applog())
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
    write_version()
    await asyncio.create_task(write_last_channel(ctx.channel.id))
    await asyncio.create_task(log(f"Restart", ctx))
    restart_bot()

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shutting down...")
    write_version()
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
        file.write(id)
    await ctx.send("done")

bot.run(token)
