import asyncio, discord, os, sys
from discord.errors import Forbidden, HTTPException, NotFound
from collections import Counter
from discord.ext import commands
from discord.utils import get
# import help_cmd
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
            if ay != "" and len(ay) < 15:
                t.append(ay)
        return t
bot = commands.Bot(command_prefix=get_prefix(), owner_ids=get_owners())
bot.remove_command('help')

@bot.event
async def on_ready():
    print("logged in")
    ch = await bot.fetch_channel(843773991055654926)
    await ch.send("online")
guild = bot.get_guild(843773991055654923)

@bot.listen()
async def on_message(msg):
    pass
##########################################################################
################################## Help ##################################
################################# Command ################################
##########################################################################

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
async def blacklist(ctx):
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

##########################################################################
################### some tiny dependant functions ########################
#################### for good and happy working ##########################
##########################################################################
async def log(content):
    try:
        content = str(content)
        with open(r"config\log.txt", "a") as file:
            file.write(content)
        with open(r"config\logch.txt") as file:
            x = int(file.read())
        ch = bot.get_channel(x)
        if ch != None:
            await ch.send(content)
            return
        else:
            ch = bot.fetch_channel(x)
            if ch != None:
                await ch.send(content)
                return
        return False
    except Exception as e:
        print(e)

def add_question_func(cat, ques):
    try:
        with open(fr"questions\{cat}.txt", "a") as file:
            file.write(ques)
        asyncio.create_task(log(f"Added Question:\n{ques}\nin category {cat}"))
    except Exception as e:
        print(e)
        asyncio.create_task(log(f"{e}"))

def remove_question(cat, ques):
    with open(fr"questions\{cat}.txt", "a") as file:
        file_source = file.read()
        file.write(file_source.replace(f"{ques}", ""))
    asyncio.create_task(log(f"Removed Question:\n{ques}\nfrom category {cat}"))

def get_id_from_mention(mention):
    return int(''.join(x for x in mention if x.isdigit()))

def write_log_channel(chid):
    with open(r"config/logch.txt", "w") as f:
        f.write(chid)
    asyncio.create_task(log(f"set {chid} to log"))

def write_applog(chid):
    with open(r"config/applog.txt", "w") as f:
        f.write(chid)
    asyncio.create_task(log(f"set {chid} to app log"))

def write_blacklist_user(usrid, app=None):
    usrid = get_id_from_mention(usrid)
    if app is not None:
        with open(r"bl\usr_blacklists.txt", "a") as f:
            f.write(f"{app}_{usrid}")
        asyncio.create_task(log(f"Blacklisted user {usrid} for app {app}."))
    else:
        with open(r"bl\usr_blacklists.txt", "a") as f:
            f.write(f"gbl_{usrid}")
        asyncio.create_task(log(f"Blacklisted user {usrid} globally."))

def write_blacklist_role(rlid, app=None):
    rlid = get_id_from_mention(rlid)
    if app is not None:
        with open(r"b\rl_blacklists.txt", "a") as f:
            f.write(f"{app}_{rlid}")
        asyncio.create_task(log(f"Blacklisted role {rlid} for app {app}."))
    else:
        with open(r"b\rl_blacklists.txt", "a") as f:
            f.write(f"gbl_{rlid}")
        asyncio.create_task(log(f"Blacklisted role {rlid} globally."))


def write_whitelist_user(usrid, app=None):
    usrid = get_id_from_mention(usrid)
    if app is not None:
        with open(r"bl\usr_blacklists.txt", "r+") as f:
            file_source = f.read()
            f.write(file_source.replace(f"{app}_{usrid}", ""))
        asyncio.create_task(log(f"Whitelisted user {usrid} for app {app}"))
    else:
        with open(r"bl\usr_blacklists.txt", "r+") as f:
            file_source = f.read()
            f.write(file_source.replace(f"gbl_{usrid}", ""))
        asyncio.create_task(log(f"Whitelisted user {usrid} for app {app}"))

def write_whitelist_role(rlid, app=None):
    rlid = get_id_from_mention(rlid)
    if app is not None:
        with open(r"bl\rl_blacklists.txt", "r+") as f:
            file_source = f.read()
            f.write(file_source.replace(f"gbl_{rlid}", ""))
        asyncio.create_task(log(f"Globally whitelisted {return_name_of_role(rlid)}"))
    else:
        with open(r"bl\rl_blacklists.txt", "r+") as f:
            file_source = f.read()
            f.write(file_source.replace(f"{app}_{rlid}", ""))
        asyncio.create_task(log(f"Whitelisted role {rlid} for app {app}"))


def get_applog():
    with open(r"config\applog.txt") as file:
        return int(file.read())

def get_app_role(app):
    with open(r"config\app_role.txt") as file:
        if app not in file.read():
            return
        else:
            for a in file.readlines():
                if app in a:
                    return (a.split("_"))[-1]

async def acc_app(ctx, app, usrid):
    try:
        usr = await bot.get_user(usrid)
        rl = get(ctx.guild.roles, id=(int(get_app_role(app))))
        await usr.add_roles(rl)
    except:
        pass

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

async def return_name_of_role(id):
    role = guild.get_role(id)
    return role.name

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

@bot.command(name="set_log_channel", aliases = ["slc"])
@commands.is_owner()
async def set_log_channel(ctx, channel):
    channel = get_id_from_mention(channel)
    try:
        sa = await bot.fetch_channel(int(channel))
        if isinstance(sa, discord.TextChannel):
            if len(str(channel)) == 18:
                try:
                    await sa.send(embed=em)
                    try:
                        write_log_channel(str(channel))
                        await ctx.send(f"I configured <#{channel}> to log everything other than applications!")
                        asyncio.create_task(log(f"{ctx.author.id} : {ctx.author.name} set <#{channel}> as log channel"))
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


@bot.command(name="set_app_channel", aliases=['sac'])
@commands.is_owner()
async def write_app_channel(ctx, chid):
    channel = get_id_from_mention(chid)
    try:
        sa = await bot.fetch_channel(int(channel))
        if isinstance(sa, discord.TextChannel):
            if len(str(channel)) == 18:
                try:
                    await sa.send(embed=em)
                    try:
                        write_applog(str(channel))
                        await ctx.send(f"I configured <#{channel}> to log applications!")
                        asyncio.create_task(log(f"{ctx.author.id} : {ctx.author.name} set <#{channel}> as application log channel"))
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
async def add_question(ctx, cat, *, abc):
    abc = f"{abc}\n"
    try:
        add_question_func(cat, abc)
        await ctx.send(f"Added question `{abc}` in category `{cat}`")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="rem_question", aliases = ["rem", "remove", "remq"])
@commands.is_owner()
async def rem_question(ctx, cat, *, ques):
    ques = f"{ques}\n"
    try:
        await remove_question(cat, ques)
        await ctx.send(f"Removed question `{ques}` in category `{cat}`")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="whitelist", aliases=['wl'])
@commands.is_owner()
async def whitelist(ctx, id, app=None):
    try:
        bot.fetch_user(id)
        write_whitelist_user(id, app)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
    except NotFound:
        write_whitelist_role(id, app)

@bot.command(name="blacklist", aliases=['bl'])
@commands.is_owner()
async def blacklist(ctx, id, app=None):
    try:
        bot.fetch_user(id)
        write_blacklist_user(id, app)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
    except NotFound:
        write_blacklist_role(id, app)

@bot.command(name="add_req", aliases=['ar'])
@commands.is_owner()
async def add_req(ctx, req, app=None):
    req = get_id_from_mention(req)
    try:
        guild.get_role(req)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
        return
    except NotFound:
        await ctx.send("I am taking only roles as requirements as of now.")
        return

    if app != None:
        det = f"{app}_{req}"
        with open(r"config\req.txt") as file:
            if det in str(file.readlines()):
                await ctx.send("This is already a requirement.")
                return
            else:
                with open("req.txt", "a") as file:
                    file.write(det)
                await ctx.send(f"Users will now require {await return_name_of_role(req)} to apply for {app}.")
    else:
        det = f"general_{req}"
        with open(r"config\req.txt") as file:
            if det in str(file.readlines()):
                await ctx.send("This is already a requirement.")
                return
            else:
                with open("req.txt", "a") as file:
                    file.write(det)
                await ctx.send(f"Users will now require {await return_name_of_role(req)} to apply for any app.")


@bot.command(name="remove_req", aliases=['rr']) 
@commands.is_owner()
async def remove_req(ctx, app, req):
    req = get_id_from_mention(req)
    try:
        guild.get_role(req)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
        return
    except NotFound:
        await ctx.send("I am taking only roles as requirements as of now.")
        return
    det = f"{app}_{req}"
    with open(r"config\req.txt") as file:
        if det not in str(file.readlines()):
            await ctx.send("This was never a requirement.")
            return
        else:
            with open(r"config\req.txt", "r+") as f:
                file_source = f.read()
                f.write(file_source.replace(f"{det}", ""))
            await ctx.send(f"Users will no longer require {await return_name_of_role(req)} to apply for {app}.")

@bot.command(name="add_owner", aliases=['ao'])
@commands.is_owner()
async def add_owner(ctx, id):
    id = get_id_from_mention(id)
    with open(r"config\owners.txt", "a") as file:
        file.write(id)

@bot.command(name="rem_owner", aliases=['ro'])
@commands.is_owner()
async def add_owner(ctx, id):
    with open(r"config\owners.txt", "a") as file:
        file_source = file.read()
        file.write(file_source.replace(f"{id}", ""))

@bot.command(name="set_prefix", aliases=['sp'])
async def set_prefix(ctx, new_prefix):
    with open(r"config\prefix.txt", "w") as file:
        file.write(new_prefix)

@bot.command(name="consider")
async def consider(ctx, app, usrid, msg=None):
    usr = bot.get_user(usrid)
    if msg != None:
        await usr.send(f"Your application for {app} is being considered. Also, {msg}")
    else:
        await usr.send(f"Your application for {app} is being considered.")
    await log(f"{ctx.author.id} ({ctx.author.name}) considered {usrid}'s application for {app}")

@bot.command(name="accept")
async def consider(ctx, app, usrid, msg=None):
    usr = bot.get_user(usrid)
    if msg != None:
        await usr.send(f"Your application for {app} has been accepted. Also, {msg}")
    else:
        await usr.send(f"Your application for {app} has been accepted.")
    try:
        await acc_app(ctx, app, usrid)
        await ctx.send("Added role to user")
    except:
        await ctx.send("ok")

@bot.command(name="reject", aliases=["deny", "decline"])
async def consider(app, usrid, msg=None):
    usr = bot.get_user(usrid)
    if msg != None:
        await usr.send(f"Your application for {app} has been rejected. Also, {msg}")
    else:
        await usr.send(f"Your application for {app} has been rejected.")

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

@bot.command(name="dump_questions", aliases=['dump', 'questions', 'dumpq'])
@commands.is_owner()
async def dump_questions(ctx, cat=None):
    if cat != None:
        try:
            with open(fr"questions\{cat}.txt") as file:
                await ctx.send(file.read())
        except FileExistsError:
            await ctx.send("No such category!")
        except Exception as e:
            await ctx.send(e)
    else:
        emb = discord.Embed(title="All Questions", description="All categories and their questions.")
        for fl in next(os.walk("questions"), (None, None, []))[2]:
            with open(fr"questions\{fl}") as file:
                if file.readlines != "":
                    emb.add_field(name=fl.replace(".txt", ""), value=file.read(), inline=False)
                else:
                    emb.add_field(name=fl.replace(".txt", ""), value=file.read(), inline=False)
                await ctx.send(embed=emb)

@bot.command(name="dump_req", aliases=['dumpr', 'requirements', 'reqs'])
@commands.is_owner()
async def dump_req(ctx, cat=None):
    if cat != None:
        try:
            with open(fr"config\{cat}.txt") as file:
                await ctx.send(file.read())
        except FileExistsError:
            await ctx.send("No such category!")
        except Exception as e:
            await ctx.send(e)
    else:
        emb = discord.Embed(title="All Questions", description="All categories and their questions.")
        for fl in next(os.walk("questions"), (None, None, []))[2]:
            with open(r"config\req.txt") as file:
                if file.read().replace("\n", "") != "":
                    ahi = file.readlines()
                    for ah in ahi:
                        x = ah.split("_")
                        emb.add_field(name=x[0], value=(await return_name_of_role(x[1])), inline=False)
                await ctx.send(embed=emb)

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

#################################################
############## Basically all of the #############
############## Actual Bot Commands ##############
################# For Public Pog ################
#################################################
@bot.command(name="raise_er")
async def raise_er(ctx, *, context=None):
    try:
        me = await bot.fetch_user(736147895039819797)
        await me.send(f"User {ctx.author.id} raised error in server {ctx.message.guild} with context: {context}\nAnd{ctx.message.jump_url}")
        await ctx.send("The author of the bot has been notified of the error raised.")
    except Exception as e:
        await me.send(f"{ctx.message.jump_url}\n{e}")

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
    restart_bot()

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shutting down...")
    await bot.close()

@bot.command()
@commands.is_owner()
async def disable(ctx, command):
    command = bot.get_command(command)
    if not command.enabled:
        return await ctx.send("This command is already disabled.")
    command.enabled = False
    await ctx.send(f"Disabled {command.name} command.")

@bot.command()
@commands.is_owner()
async def enable(ctx, command):
    command = bot.get_command(command)
    if command.enabled:
        return await ctx.send("This command is already enabled.")
    command.enabled = True
    await ctx.send(f"Enabled {command.name} command.")


bot.run(token)
