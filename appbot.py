import json
import discord
import asyncio
import os
import sys
from add_question import main as add_question
from add_question import replace_line as rl
from discord.ext import commands
import config

bot = commands.Bot(help_command=None, command_prefix="!!")

@bot.event
async def on_ready():
    print("logged in")
    startup_channel = await bot.fetch_channel(843773991055654926)
    await startup_channel.send("online")

em = discord.Embed(title="Test Embed", description="Just ensuring i cant send messages and embeds here")

def write_log(chid):
    with open("config.py", "r") as f:
        for a in f.readlines():
            if "log_channel = " in a:
                rl("config.py", 0, f"log_channel = {chid}")

def write_app(chid):
    with open("config.py", "r") as f:
        for a in f.readlines():
            if "log_channel = " in a:
                rl("config.py", 1, f"apps_channel = {chid}")
def write_blacklist_user(chid):
    with open("blacklists.py", "r") as f:
        for a in f.readlines():
            if "blacklisted_users = [" in a:
                a = a.replace("]", f", {chid}]")
                rl("blacklists.py", 0, a)
def write_whitelist_user(usrid):
    with open("blacklists.py", "r") as f:
        for a in f.readlines():
            if "blacklisted_users = [" in a:
                a = a.replace(f", {usrid}", "")
                rl("blacklists.py", 0   , a)
def write_whitelist_role(rolid):
    with open("blacklists.py", "r") as f:
        for a in f.readlines():
            if "blacklisted_users = [" in a:
                a = a.replace(f", {rolid}", "")
                rl("blacklists.py", 1, a)
def write_blacklist_role(rolid):
    with open("blacklists.py", "r") as f:
        for a in f.readlines():
            if "blacklisted_roles = [" in a:
                a = a.replace("]", f", {rolid}]")
                rl("blacklists.py", 1, a)

@bot.command(name="set_log_channel", aliases = ["slc"])
@commands.has_permissions(manage_messages=True)
async def set_log_channel(ctx, channel):
    channel = int(channel.replace(" ", ""))
    if len(str(channel)) == 18:
        try:
            aio = bot.get_channel(channel)
            try:
                await aio.send(embed=em)
                write_log(channel)
                await ctx.send(f"I configured <#{channel}> to log applications")
            except:
                await ctx.send("The Bot appears to be unable to post messages and/or messages in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel")
        except:
            await ctx.reply("The bot can not reach the channel, Please ensure the argument given is the snowflake ID of the channel.")
    else:
        await ctx.send(f"Channel argument has been improperly passed, Please ensure the argument given is the snowflake ID of the channel.")

@bot.command(name="questions")
async def questions(ctx, cat):
    try:
        with open(f"questions/{cat}.txt") as file:
            await ctx.send(file.read())
    except FileExistsError:
        await ctx.send("No such category!")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="raise_er")
async def raise_er(ctx, *, context=None):
    try:
        me = await bot.fetch_user(736147895039819797)
        await me.send(f"User {ctx.author.id} raised error in server {ctx.message.guild} with context: {context}")
        await ctx.send("The author of the bot has been notified of the error raised.")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="set_question", aliases = ["sq"])
async def set_question(ctx, cat, *, ques):
    try:
        add_question(cat, ques)
        await ctx.send(f"Added question `{ques}` in category `{cat}`")
    except Exception as e:
        await ctx.send(e)

@bot.command(name="set_app_channel", aliases=['sac'])
async def set_app_channel(ctx, chid):
    channel = int(chid.replace(" ", ""))
    if len(str(channel)) == 18:
        try:
            aio = bot.get_channel(channel)
            try:
                await aio.send(embed=em)
                write_log(channel)
                await ctx.send(f"I configured <#{channel}> to take applications")
            except:
                await ctx.send("The Bot appears to be unable to post messages and/or messages in the specified channel, Please Ensure I am allowed to post embeds and messages in that channel")
        except:
            await ctx.reply("The bot can not reach the channel, Please ensure the argument given is the snowflake ID of the channel.")
    else:
        await ctx.send(f"Channel argument has been improperly passed, Please ensure the argument given is the snowflake ID of the channel.")

@bot.command(name="list")
async def list(ctx, black_or_white, role_or_user, id):
    if "black" in black_or_white:
        if "role" in role_or_user:
            write_blacklist_role(id)
            await ctx.send(f"Anyone with role <@&{id}> will not be able to apply. sedlyf4them")
        elif "user" in role_or_user:
            write_blacklist_user(id)
            await ctx.send(f"User <@{id}> will not be able to apply. sedlyf4them")
    if "white" in black_or_white:
        if "role" in role_or_user:
            write_whitelist_role(id)
            await ctx.send(f"Anyone with role <@&{id}> will now be able to apply. gg")
        elif "user" in role_or_user:
            write_whitelist_user(id)
            await ctx.send(f"User <@{id}> will now be able to apply, gg")

@bot.command(name="remove_questions", aliases=["rq"])
async def remove_questions(ctx, cat, ques_no):
    with open("questions.py", "r") as file:
        x = file.readlines()
        for i in range(len(x)):
            if f"{cat} = [" in x[i]:
                return
            else:
                pass

def restart_bot(): 
  os.execv(sys.executable, ['python'] + sys.argv)

@bot.command(name="restart")
@commands.is_owner()
async def restart(ctx):
    await ctx.send("Restarting the bot...")
    restart_bot()

@bot.command(nam="toggle")
async def toggle(ctx, on_or_off, app):
    details = f"{ctx.message.guild.id}_{app}"
    with open("active_apps.txt") as file:
        x = file.readlines()
    with open("active_apps.txt", "a") as f:
        for a in range(len(x)):
            if on_or_off == "on":
                if details in x[a]:
                    return
                elif details not in str(x):
                    f.write(f"\n{details}")
                    await ctx.send("This application is now accepting.")
                    return
                else:
                    pass
            elif on_or_off == "off":
                if details not in str(x):
                    return
                elif details in x[a]:
                    rl("active_apps.txt", a, "")
                    await ctx.send("This application is now not accepting.")
                    return
                else:
                    pass


def check(ctx):
    with open("blacklists.py") as file:
        x = file.readlines()
        x = str(x)
        roles_ids = []
        for y in ctx.author.roles:
            roles_ids.append(y.id)
        if str(ctx.author.id) in x:
            return False
        else:
            for y in ctx.author.roles:
                if str(y.id) in x:
                    return False

@bot.command(name="add_req")
async def add_req(ctx, app, req):
    with open("req.txt") as file:
        if f"{ctx.message.guild.id}_{app}_{req}" in str(file.readlines()):
            await ctx.send("This is already a requirement.")
            return
        else:
            with open("req.txt", "a") as file:
                file.write(f"{ctx.message.guild.id}_{app}_{req}")

@bot.command(name="remove_req")
async def remove_req(ctx, app, req):
    with open("req.txt") as file:
        if f"{ctx.message.guild.id}_{app}_{req}" not in str(file.readlines()):
            await ctx.send("This was never a requirement.")
            return
        else:
            for x in file.readlines():
                if f"{ctx.message.guild.id}_{app}_{req}" in x:
                    rl("req.txt", x, "")
                    return
                else:
                    pass

async def get_id(ctx):
    try:
        return ctx.message.mentions[0].id
    except:
        pass



def common_member(a, b):
    return(any(i in a for i in b))

def get_reqs(ctx, app=None):
    some_temp_list = []
    with open("req.txt") as file:
        ah = file.readlines()
        for ahi in ah:
            if f"{ctx.message.guild.id}_{app}" in ahi:
                some_temp_list.append(ahi.split("_")[-1])

def get_role_ids(ctx):
    roles_ids = []
    for y in ctx.author.roles:
        roles_ids.append(y.id)

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

@bot.command(name="shutdown")
@commands.is_owner()
async def shutdown(ctx):
    await ctx.send("shutting down...")
    await bot.close()

@bot.command()
@commands.is_owner()
async def disable(self, ctx, command):
    command = self.bot.get_command(command)
    if not command.enabled:
        return await ctx.send("This command is already disabled.")
    command.enabled = False
    await ctx.send(f"Disabled {command.name} command.")

@bot.command()
@commands.is_owner()
async def enable(self, ctx, command):
    command = self.bot.get_command(command)
    if command.enabled:
        return await ctx.send("This command is already enabled.")
    command.enabled = True
    await ctx.send(f"Enabled {command.name} command.")


bot.run(config.token)