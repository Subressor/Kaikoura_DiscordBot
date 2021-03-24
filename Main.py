# Welcome to the code for the Kaikoura Guild Server's Discord Bot!
# I've tried my best to comment out as many lines as possible for easy comprehension. This is the first bot I've written so it was a learning exerise for me as well as a functional bot to use in my guilds discord server
# Please check te Github for the latest version and the Readme for how it works / features

# Boring package loading stuff used by the code
import os

import discord, asyncio
from discord.ext import commands
from datetime import datetime, timedelta
from time import sleep

# Logging setup to a discord.log file
# TODO - Make this more comprehensive. Write printf messages into debug
import logging
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Loads environment Variables from .env file. This is NOT source controlled
from dotenv import load_dotenv
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVERNAME = os.getenv('DISCORD_SERVER_NAME')
SERVERID = os.getenv('DISCORD_SERVER_ID')

# Sets up intents, which is some new fancy way of making large data api calls (like get all users in server)
intents = discord.Intents.all()
intents.members = True
bot = commands.Bot(command_prefix='!', intents=intents)

# On_Ready, called when the client is done preparing the data received from Discord. Usually after login is successfull and the client.guilds and co. are filled up.
# WARNING - CAN BE CALLED MULTIPLE TIMES, AND NOT NECESSARILY THE FIRST THING EXECUTED
@bot.event
async def on_ready():
    # Check that we connected to the Server Ok
    print(f'{bot.user.name} has connected to Discord!')

    # Starts the DM Chain to BlakeTest
    guild = bot.get_guild(int(SERVERID))
    testmember = guild.get_member_named("BlakeTest")
    print(f'{testmember} member found, and a DM has been sent')
    await testmember.create_dm()
    await testmember.dm_channel.send("https://memegenerator.net/img/instances/66094741.jpg")
    embed=discord.Embed(title="Hey, welcome to the discord server for **Kaikoura!**", description="We're a UK based WoW guild that does social and cutting edge level PvE and PvP content", color=0xFF5733, inline=False)
    embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    embed.add_field(name="Please change your Discord server nickname to your in-game WoW name", value="This is so that we know who you are. You can do this by joining a channel on the server, right clicking on your name and selecting 'change nickname' \n \n Social degenerates, please read the 'rules' pinned in the #rules channel.\n",  inline=False)
    embed.add_field(name="If you have joined the server for a specific event...", value="Please join an empty public channel and wait patiently to be moved, or the guildie will come to join you", inline=False)
    embed.add_field(name="If you would like to apply to join the guild...", value="Please reply to this DM with **'!ApplyToJoin'** and this bot will take you through the application questions. Please be on your main PC and have ~10mins free to complete the questions \n \n Any issues or problems, please reach out to an officer!", inline=False)
    await testmember.dm_channel.send(embed=embed)


# Welcome message to new server-joiners
@bot.event
async def on_member_join(member):
    
    guild = bot.get_guild(int(SERVERID))
    public_channel = discord.utils.get(guild.text_channels, name = "public-general")

    await member.create_dm()

    # Can't have any joiners without some good old doge memes
    # Try to send a simple message first and do a check to see if we can actually DM the user. If not, we'll post a ping in Public
    try:
        await member.dm_channel.send("https://memegenerator.net/img/instances/66094741.jpg")
    except discord.Forbidden:
        print(f'Cannot DM the newly joined user ({member.name}), do they have closed DMs / not accepting DMs?')
        return await public_channel.send("Hi {}, I can't seem to DM you with some info about the guild. Do you have closed DMs?".format(member.mention))

    # Embedded discord message, basically a fancy formatted message in python syntax. /n is new line (neater than triple quotes)
    embed=discord.Embed(title="Hey, welcome to the discord server for **Kaikoura!**", description="We're a UK based WoW guild that does social and cutting edge level PvE and PvP content", color=0xFF5733, inline=False)
    embed.set_author(name=bot.user.display_name, icon_url=bot.user.avatar_url)
    embed.add_field(name="Please change your Discord server nickname to your in-game WoW name", value="This is so that we know who you are. You can do this by joining a channel on the server, right clicking on your name and selecting 'change nickname' \n \n Social degenerates, please read the 'rules' pinned in the #rules channel.\n",  inline=False)
    embed.add_field(name="If you have joined the server for a specific event...", value="Please join an empty public channel and wait patiently to be moved, or the guildie will come to join you", inline=False)
    embed.add_field(name="If you would like to apply to join the guild...", value="Please reply to this DM with '!ApplyToJoin' and this bot will take you through the application questions. - Please be on your main PC and have ~10mins free to complete the questions \n \n Any issues or problems, please reach out to an officer!", inline=False)
    
    await member.dm_channel.send(embed=embed)

    # DEBUG
    print(f'{member} has joined the server. A welcome message has been sent')

# Starts the questionaire-style application process
# TODO - Only allow applicants to start this process with a DM command. The bot currently accepts this command from all channels it has access to
# TODO - Check to see if the applicant already has member-specific roles to prevent internal spam
# TODO - Check to see if the applicant has already submitted an application recently to prevent external spam. Maybe by checking through the submission channel and seeing if their UserID comes up?
# TODO - Migrate the question list into some sort of structured environment variable, perhaps a JSON?
# TODO - Only ask certain questions based off the response from another question (e.g. don't ask raider-level questions if the person only wants to be a social)
@bot.command()
async def ApplyToJoin(ctx):
    """Apply to join the guild."""

    # DEBUG
    print(f'{ctx.author} has applied to join the guild using the !ApplyToJoin command')

    # Set the channels to post the application to and the direct messages to
    guild = bot.get_guild(int(SERVERID))
    dm_channel = await ctx.author.create_dm()
    submit_channel = discord.utils.get(guild.text_channels, name = "officer-applications")

    # DEBUG
    print(f'{submit_channel} will be used to post the completed application to')

    # Input the list of questions to ask the applicant (Python Array). This can be variable'd and expanded upon
    # TODO - Migrate this list out to an environment variable. Perhaps a JSON?
    q_list = [
        'So that I know what kind of questions to ask you, can you tell me what activites in the guild you\'re applying for / interested in? Please use the following keywords: \n - Social \n - Social-Raiding \n - Mythic-Raiding \n - Mythic-Dungeons \n - Social-PvP \n - Glad-PvP',
        'Let\'s begin with a little bit about you. What\'s your real-life first name?',
        'How old are you?',
        'Where are you from?',
        'How good is your English?',
        'Does something swing between your legs?',
        'What do you do to bring home the bacon?',
        'In a word or two, how would you summarise your personality?',
        'In a word or two, how would you summarise your gaming persona (How are you as a gamer?)?',
        'Thanks for that, Let\'s talk about your gamer prowess now. What\'s your main characters name? Please type it exactly as it appears',
        'Main Characters Class / Spec?',
        'Do you have any logs for your character? If so, please link them below',
        'Any good with your characters other specs? If so, how profficient?',
        'What\'s your BTag? (Include the #xxxx Number please)',
        'Summarise your PvE history (BRIEFLY). How long have you been playing for, at what level, how good are you?',
        'How many Cutting Edge (CE) and Ahead of the Curve (AoTC) achievements do you have on your account? (No we don\'t care about your old accounts that you sold)',
        'Summarise your PvP history (BRIEFLY). How long have you been playing for, at what level, how good are you?',
        'Do you click any of your characters abilities?',
        'Do you have any alts at a similar level to your main? If so, please detail here',
        'Are you a snowflake?',
        'Can you take yo-momma banter?',
        'We are not a PC guild. We will take the absolute piss out of everything about you. Are you cool with that',
        'Alright Sweet. And FINALLY, anything serious we need to know about? Any medical conditions, health issues, things that trigger you, etc.',
    ]
    # The array of answers. Dynamically generated to match the size of the question array.
    a_list = ['No Response Detected'] * len(q_list)

    # Pre-interview question to get them lubed up
    try:
        await ctx.author.send("Thanks for your interest in the guild! The application process has now started. You have maximum of 5 minutes to answer each question, try to keep your answers concise. If you take too long to respond to a question, the application will time-out and you will have to start again. If you run into any issues, please DM a member of the officer team.")
    except discord.Forbidden:
        print(f'Cannot DM the user interested in applying ({ctx.author}), do they have closed DMs / not accepting DMs?')
        return await ctx.send("Cannot DM the user interested in applying, do they have closed DMs / not accepting DMs?")

    # Just a natural break so that applicant can read the above before submitting the first question
    sleep(5)

    # Absolutely no idea what this does, some sort of check?
    def check(m):
        return m.author == ctx.author and m.channel == ctx.author.dm_channel

    # Question asking loop. This goes through the array of questions we prepared earlier and askes them all, waiting on a response for each before moving on. Responses are saved to the answer array
    for x in range(len(q_list)):
        await ctx.author.send(q_list[x])
        try:
            a_list[x] = await bot.wait_for("message", timeout=300, check=check)
        except asyncio.TimeoutError:
            print(f'{ctx.author} timed out their application, please tell them to try again')
            return await ctx.send("you took too long. try again, please.")
    
    # Truncating answers and questions to not go over character limits imposed by the discord format embedded message
    # TODO - Make this consume less lines of code
    for x in range((len(q_list))):
        temp = q_list[x]
        if len(temp) > 250:
            temp = temp[:100]
            temp = temp + '...'
            q_list[x] = temp
            # DEBUG print('question {x}, which was "{q_list[x]}" was not in length. It has now been changed!')
        # else:
            # DEBUG print('question {x}, which was "{q_list[x]}" was in length!') 
    for x in range((len(a_list))):
        temp = a_list[x].content
        if len(temp) > 200:
            temp = temp[:200]
            temp = temp + '...'
            a_list[x].content = temp
            # DEBUG print('answer {x}, which was "{a_list[x]}" was not in length. It has now been changed!')
        # else:
            # DEBUG print('answer {x}, which was "{a_list[x]}" was in length!')

    # Application finished. Bundle the responses into an embedded post for the officers to perv at.
    embed = discord.Embed(title=f"New application from {ctx.author.name}#{ctx.author.discriminator}, UserID - {ctx.author.id}", color=0xFF5733, timestamp=datetime.now())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"{ctx.author.name}#{ctx.author.discriminator} ({ctx.author.id})")
    for x in range((len(q_list))):
        embed.add_field(name=q_list[x], value=a_list[x].content, inline=False)

    await submit_channel.send(embed=embed)
    await ctx.author.send("Your application has been sent to the guilds officers, thank you for your time! We will review it and get back to you as soon as possible. Please stay connected to the guild server and we will reach out to you soon with a decision. Any questions in the meantime, please don't hesiate to reach out!")

    # Changes the applicants nickname to be the same as the main of their in-game characters name as they've written in the application. This makes finding them easier
    member = await guild.fetch_member(ctx.author.id)
    await member.edit(nick=a_list[9].content)

    # DEBUG
    print(f'({ctx.author.name}) has completed an application and it has been posted into the officer channel! Can I haz a cookie now? :-3')


@bot.command(pass_context=True)
async def Accept(ctx, userid):
    """Accept an application from a user based off their UserID."""
    guild = bot.get_guild(int(SERVERID))
    submit_channel = discord.utils.get(guild.text_channels, name = "officer-applications")
    welcome_channel = discord.utils.get(guild.text_channels, name = "guild-general")

    # We get a member reference here for the applicant instead of a user reference. This allows us to do more guild-specific stuff like roles
    member = await guild.fetch_member(userid)
  
    # DEBUG
    print(f'A command from {ctx.author} has been received to accept the application with ID {userid}')

    # Check if the member was found, and exit the function if not
    if member is not None:
        print(f'User found! {member.name}')
    else:
        await submit_channel.send(f'User with ID {userid} not found! Maybe they left the server? Or')
        return

    # Check if the approver has the manage permissions role, and exit the funtion if not
    if ctx.author.guild_permissions.manage_roles:
        dm_channel = await member.create_dm()
    else:
        await submit_channel.send(f'Command invoker does not have required permissions to approve the applicant. GTFO NOOB')
        return

    # Finds the role to promote to user to (member in our case), and promotes the user
    # TODO - Permissions check loop for the bot to make sure the bot can manage roles
    role = discord.utils.get(guild.roles, name='Member')
    await member.add_roles(role)

    # Checks passed. Send a nice embedded message to the applicant with the introduction and To-Do list
    await member.dm_channel.send("https://memegenerator.net/img/instances/78053019.jpg")

    embed = discord.Embed(title=f"Your application has been successful, welcome to Kaikoura! Please read the below instructions for your next steps:", color=0xFF5733, timestamp=datetime.now())
    embed.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    embed.set_footer(text=f"Application approved by {ctx.author.name} at {datetime.now()}")
    embed.add_field(name="Get invited to the guild in-game", value="Please reach out to an officer who may be online, or use the in-game guild recruitment tool and search for **Kaikoura**.", inline=False)
    embed.add_field(name="Check & Change your Discord Nickname to your in-game characters name", value="This is server specific, and for us to know who you are easily! You can do this by right-clicking your name on the server list on the right hand side and selecting 'nickname'. It won't alter your discords main nickname or names on any of your other servers.", inline=False)
    embed.add_field(name="In-Game Calendar for signups", value="We use the in-game calendar to manage signups for events. PLEASE check it now and make it a habbit to update this with your availability. If you want to come and know you can make it, select 'Signup'. If you want to come but don't know if you can make it or might be late, sign up as 'Tentative'. If you can't make it / don't want to come, DON'T SIGN UP! It helps the officer team out a lot to know who's coming to what.", inline=False)
    embed.add_field(name="Check out the guild bible", value="there is a specific text channel in the members section called 'guild-bible'. This contains a link to a google slides doc that is the central place for all of our guild info. Please take a look at it over the next week or so and let me know if you have any questions.", inline=False)
    embed.add_field(name="Mute the 'guild bot commands' channel", value="We have a channel specifically for giving commands to the guild bots (including me!). We suggest you mute this channel to avoid unecessary spam. If you decide to mute the whole server, please leave @mentions unmuted as we use this to notify members for events starting etc.", inline=False)
    
    await member.dm_channel.send(embed=embed)
    
    # Generic welcome message
    await welcome_channel.send(f'Good news everybody, <@{userid}> has made it through the gruelling application process and is here to get carried. Give him a Whaaalecum and good yo-momma joke')
    
    # Confirmation Message
    await submit_channel.send(f'If the code made it this far, the {member.name} has been accepted, given a role and the welcome/introduction message by {ctx.author.name}! Hurrah!')

    #Debug
    print(f'If the code made it this far, the {member.name} has been accepted, given a role and the welcome message by {ctx.author.name}! Hurrah!')


# I think this is the bots inbuilt error handling thing. Found the arguements and code too complex, so just error handled in the events themselves
# TODO - Move error handling logic out to here
@bot.event
async def on_error(event, *args, **kwargs):
    with open('err.log', 'a') as f:
        if event == 'on_message':
            f.write(f'Unhandled message: {args[0]}\n')
        else:
            raise



bot.run(TOKEN)
