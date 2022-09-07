import os
import time
import random
import datetime
import colorama
from captcha.image import ImageCaptcha
import discord
import mysql.connector
from discord.ext import commands

prefix = "xdb!"
needed_intents = discord.Intents.all()
client = commands.Bot(command_prefix = prefix, intents=needed_intents)
bottoken = "changetoken"
bannerdate = datetime.datetime.today()

#colors
yellowcol = colorama.Fore.LIGHTYELLOW_EX
cyancol = colorama.Fore.CYAN
purplecol = colorama.Fore.MAGENTA
greencol = colorama.Fore.GREEN
redcol = colorama.Fore.LIGHTRED_EX
resetcol = colorama.Fore.RESET

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="changemysqlpass",
    database="xdb-db"
)

cursor = mydb.cursor(dictionary=True)

banner = f"""

                   {purplecol}    ▄  ██▄{cyancol}   ███   {resetcol}
                   {purplecol}▀▄   █ █  {cyancol}█  █  █  {resetcol}
                   {purplecol}  █ ▀  █  {cyancol} █ █ ▀ ▄ {resetcol}
                   {purplecol} ▄ █   █  {cyancol}█  █  ▄▀ {resetcol}
                   {purplecol}█   ▀▄ ███{cyancol}▀  ███   {resetcol}
                   {purplecol} ▀        {cyancol}         {resetcol}

            {redcol}XDB{resetcol} Database Recollection Tool.
"""

@client.event
async def on_ready():
    os.system("clear")
    print(banner)
    print(f"{yellowcol}{bannerdate}{resetcol} {cyancol}INFO{resetcol}  [ Connecting To The XDB Database ]")
    time.sleep(3)
    print(f"{yellowcol}{bannerdate}{resetcol} {cyancol}INFO{resetcol}  [ Loading Database Files ]")
    time.sleep(2)
    print(f"{yellowcol}{bannerdate}{resetcol} {greencol}SUCCESS{resetcol}  [ XDB Is Online ]")
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send("You're On Cooldown, Try Again In {:.2f}s".format(error.retry_after))
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def search(ctx, *input_):
    cursor.execute(f"SELECT PLAN from test where ID = {ctx.author.id}")
    rows = cursor.fetchall()
    for row in rows:
        checker = row["PLAN"]
        if checker == "free":
            await ctx.send("You Need A Membership")
        else:
            await ctx.send("This Could Take A Little While..")
            firstID = str(random.randint(1,10000))
            finalID = str(random.randint(1,10000))
            os.system(f"grep " + (str(' '.join(input_) +f" * | uniq > first-{firstID}.txt")))
            f = open(f"first-{firstID}.txt", "r").read()
            os.system(f"grep -v 'sirius.py' first-{firstID}.txt > final-{finalID}.txt")
            file_path = f'final-{finalID}.txt'
            if os.stat(file_path).st_size == 0:
                await ctx.send("XDB Found Nothing..")
                os.system(f"rm final-{finalID}.txt; rm first-{firstID}.txt")
            else:
                await ctx.send(file=discord.File(rf'final-{finalID}.txt'))
                os.system(f"rm final-{finalID}.txt; rm first-{firstID}.txt")
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def register(ctx):
    check = ctx.author.id
    #whitelist id here cuh
    if (str(check))  == "yourdiscordid":
        sql = "INSERT INTO test (ID, PLAN) VALUES (%s, %s)"
        val = (ctx.author.id, "admin")
        cursor.execute(sql, val)
        registersuccess = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
        registersuccess.add_field(name="Your Account Has Been Registered!", value=f"Your Account ID Is {ctx.author.id}")
        registersuccess.set_footer(text="XDB Recollection Service | Admin")
        await ctx.send(embed=registersuccess)
    else:
        sql = "INSERT INTO test (ID, PLAN) VALUES (%s, %s)"
        val = (ctx.author.id, "free")
        cursor.execute(sql, val)
        registersuccess = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
        registersuccess.add_field(name="Your Account Has Been Registered!", value=f"Your Account ID Is {ctx.author.id}")
        registersuccess.set_footer(text="XDB Recollection Service")
        await ctx.send(embed=registersuccess)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def check(ctx, *input_):
    cursor.execute(f"SELECT PLAN from test where ID = "+ (str(' '.join(input_) +"")))
    rows = cursor.fetchall()
    for row in rows:
        yuh = row["PLAN"]
        if yuh != "admin":
            await ctx.send("Invalid Permissions")
        else:
            accountinfo = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
            accountinfo.add_field(name="Plan Info:", value=f"This Plan Is {yuh}")
            accountinfo.set_footer(text="XDB Recollection Service")
            await ctx.send(embed=accountinfo)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def add_admin(ctx, *input_):
    cursor.execute(f"SELECT PLAN from test where ID = {ctx.author.id}")
    rows = cursor.fetchall()
    for row in rows:
        checker = row["PLAN"]
        if checker != "admin":
            await ctx.send("Invalid Permissions")
        else:
            sql = "UPDATE test SET PLAN = %s WHERE ID = %s"
            val = ("admin", ((str(' '.join(input_)))))
            cursor.execute(sql, val)
            addadminsuccess = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
            addadminsuccess.add_field(name="Success!", value=f"Account Has Been Successfully Updated To Admin")
            addadminsuccess.set_footer(text="XDB Recollection Service")
            await ctx.send(embed=addadminsuccess)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def add_paid(ctx, *input_):
    cursor.execute(f"SELECT PLAN from test where ID = {ctx.author.id}")
    rows = cursor.fetchall()
    for row in rows:
        checker = row["PLAN"]
        if checker != "admin":
            ctx.send("Invalid Permissions")
        else:
            sql = "UPDATE test SET PLAN = %s WHERE ID = %s"
            val = ("paid", ((str(' '.join(input_)))))
            cursor.execute(sql, val)
            addadminsuccess = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
            addadminsuccess.add_field(name="Success!", value=f"Account Has Been Successfully Updated To Paid")
            addadminsuccess.set_footer(text="XDB Recollection Service")
            await ctx.send(embed=addadminsuccess)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def ban(ctx, *input_):
    cursor.execute(f"SELECT PLAN from test where ID = {ctx.author.id}")
    rows = cursor.fetchall()
    for row in rows:
        checker = row["PLAN"]
        if checker != "admin":
            await ctx.send("Invalid Permissions")
        else:
            sql = "UPDATE test SET PLAN = %s WHERE ID = %s"
            val = ("banned", ((str(' '.join(input_)))))
            cursor.execute(sql, val)
@client.command()
@commands.cooldown(1, 5, commands.BucketType.user)
async def account(ctx):
    cursor.execute(f"SELECT PLAN from test where ID = {ctx.author.id}")
    rows = cursor.fetchall()
    for row in rows:
        yuh = row["PLAN"]
        if yuh == "free":
            dbaccess = "No Databases"
        elif yuh == "paid":
            dbaccess = "All Databases"
        elif yuh == "admin":
            dbaccess = "All Databases"
        accountinfo = discord.Embed(title="XDB", description="Database Recollection Service", color=0x23272A)
        accountinfo.add_field(name="Plan Info:", value=f"Your Plan Name Is '{yuh}'")
        accountinfo.add_field(name="Access Info:", value=f"Access To {dbaccess}")
        accountinfo.set_footer(text="XDB Recollection Service")
        await ctx.send(embed=accountinfo)
client.run(bottoken)