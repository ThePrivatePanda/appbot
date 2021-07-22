import json
import re
import discord
import asyncio
import os
import sys
from discord.errors import HTTPException, NotFound
from collections import Counter
from discord.ext import commands
from discord.ext.commands.core import check
import config

bot = commands.Bot(help_command=None, command_prefix="!!")

@bot.event
async def on_ready():
    print("logged in")
    await bot.fetch_channel(843773991055654926).send("online")
em = discord.Embed(title="Test Embed", description="Just ensuring i cant send messages and embeds here")

def add_question(cat, ques):
    with open(f"questions\{cat}.txt", "a") as file:
        file.write(ques)      

def remove_question(cat, ques):
    with open(f"questions\{cat}.txt", "a") as file:
        file_source = file.read()
        file.write(file_source.replace(f"{ques}", ""))

def get_id_from_mention(mention):
    return int(''.join(x for x in mention if x.isdigit()))

def write_log(chid):
    with open(r"config/logch.txt", "w") as f:
        f.write(chid)

def write_applog(chid):
    with open(r"config/applog.txt", "w") as f:
        f.write(chid)

def write_blacklist_user(app, usrid):
    with open(r"bl\usr_blacklists.txt", "a") as f:
        f.write(f"{app}_{usrid}")

def write_blacklist_role(app, rlid):
    with open(r"b\rl_blacklists.txt", "a") as f:
        f.write(f"{app}_{rlid}")

def write_whitelist_user(app, usrid):
    with open(r"bl\usr_blacklists.txt", "r+") as f:
        file_source = f.read()
        f.write(file_source.replace(f"{app}_{usrid}", ""))

def write_whitelist_role(app, rlid):
    with open(r"bl\rl_blacklists.txt", "r+") as f:
        file_source = f.read()
        f.write(file_source.replace(f"{app}_{rlid}", ""))

@bot.command(name="set_log_channel", aliases = ["slc"])
@commands.has_permissions(manage_messages=True)
async def set_log_channel(ctx, channel):
    channel = get_id_from_mention(channel)
    if len(str(channel)) == 18:
        try:
            aio = bot.get_channel(channel)
            try:
                await aio.send(embed=em)
                write_log(channel)
                await ctx.send(f"I configured <#{channel}> to log applications!")
            except:
                await ctx.send("I can't send messages and/or embeds in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel/")
        except:
            await ctx.reply("The bot can not reach the channel, check permissions.")
    else:
        await ctx.send(f"Channel argument has been improperly passed.")

@bot.command(name="questions")
async def questions(ctx, cat):
    try:
        with open(f"{cat}.txt") as file:
            await ctx.send(file.read())
    except FileExistsError:
        await ctx.send("No such category!")
    except Exception as e:
        await ctx.send(e)


@bot.command(name="raise_er")
async def raise_er(ctx, *, context=None):
    try:
        me = await bot.fetch_user(736147895039819797)
        await me.send(f"User {ctx.author.id} raised error in server {ctx.message.guild} with context: {context}\nAnd{ctx.message.jump_url}")
        await ctx.send("The author of the bot has been notified of the error raised.")
    except Exception as e:
        await me.send(f"{ctx.message.jump_url}\n{e}")

@bot.command(name="add_question", aliases = ["ad", "add"])
async def set_question(ctx, cat, *, ques):
    try:
        add_question(cat, ques)
        await ctx.send(f"Added question `{ques}` in category `{cat}`")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="set_app_channel", aliases=['sac'])
async def set_app_channel(ctx, chid):
    channel = get_id_from_mention(chid)
    if len(str(channel)) == 18:
        try:
            aio = bot.get_channel(channel)
            try:
                await aio.send(embed=em)
                write_log(channel)
                await ctx.send(f"I configured <#{channel}> to take applications!")
            except:
                await ctx.send("I can't send messages and/or embeds in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel.")
        except:
            await ctx.reply("The bot can not reach the channel, check permissions.")
    else:
        await ctx.send(f"Channel argument has been improperly passed.")


@bot.command(name="blacklist")
async def blacklist(ctx, app, id):
    try:
        bot.fetch_user(id)
        write_blacklist_user(app, id)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
    except NotFound:
        write_blacklist_role(id)

@bot.command(name="whitelist")
async def blacklist(ctx, app, id):
    try:
        bot.fetch_user(id)
        write_whitelist_user(app, id)
    except HTTPException:
        await ctx.send("Error, could you please re-run the command")
    except NotFound:
        write_whitelist_role(id)

@bot.command(nam="toggle")
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

guild = bot.get_guild(727276010600530011)

async def return_name_of_role(id):
    role = guild.get_role(id)
    return role.name

@bot.command(name="add_req")
async def add_req(ctx, app, req):
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
        if det in str(file.readlines()):
            await ctx.send("This is already a requirement.")
            return
        else:
            with open("req.txt", "a") as file:
                file.write(det)
            await ctx.send(f"Users will now require {return_name_of_role(req)} to apply.")



@bot.command(name="remove_req")
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
            await ctx.send(f"Users will no longer require {return_name_of_role(req)} to apply")
##########################################################################
############### Can The User Apply Check Functions Support ###############
################ I'm Too Lazy To Put Them In Real Function ###############
##########################################################################

def get_reqs(app):
    some_temp_list = []
    with open(r"config\req.txt") as file:
        ah = file.readlines()
        for ahi in ah:
            if f"{app}+" in ahi:
                some_temp_list.append(int(ahi.split("_")[-1]))
    return some_temp_list


def get_role_blacklists(app):
    some_temp_list = []
    with open(r"bl\blacklists.txt") as file:
        ah = file.readlines()
        for ahi in ah:
            if f"{app}_" in ahi:
                some_temp_list.append(int(ahi.split("_")[-1]))
    return some_temp_list

def common_member(a, b):
    return(any(i in a for i in b))

def get_role_ids(usrid):
    usr = bot.fetch_user(usrid)
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

##########################################################################
############### Can The User Apply Check Functions Because ###############
################ I'm Too Lazy To Put Them In Once Function ###############
##########################################################################

def is_user_blacklisted(app, usrid):
    d = f"{app}_{usrid}"
    with open(r"bl\usr_blacklists.txt") as file:
        return d in file.readlines()

def is_role_blacklisted(usrid, app):
    with open(r"bl\rl_blacklists.txt") as file:
        return common_member((get_role_ids(usrid)), get_role_blacklists(app))

def is_any_app_active():
    with open(r"config\active_apps.txt") as file:
        if str(file.read()).replace("\n", "") == "":
            return False
        else:
            return True

def meets_general_req(usrid):
    with open(r"config\req.txt") as file:
        checkInFirst(get_role_ids(usrid), get_general_req())

def can_apply_to_any(usrid):
        for app in get_active():
            checkInFirst(get_role_ids(usrid), get_reqs(app))


##########################################################################
############################# The Main Stuff #############################
############################# Because Why Not ############################
##########################################################################

def all_checks(ctx):
    with open("active_apps.txt") as file:
        if ctx.message.guild.id not in str(file.readlines()):
            return("There are no active applications in this server.")
        elif (common_member(get_role_ids(ctx), get_reqs(ctx))) == False:
            return("There are no applications that you can apply to")
    if (check(ctx)) == False:
        return("You cannot apply.")
    else:
        return("You might be worthy of applying already")

@bot.command(name="apply")
async def apply(ctx):
    await ctx.send(all_checks(ctx))




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


bot.run(config.token)