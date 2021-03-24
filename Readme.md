# About
Welcome to the code for the Kaikoura Guild Server's Discord Bot!

This was the first bot I've written using Python (Discord.py), and I'm sharing it with the community as a learning guide for those who would like to learn Python and create a bot from scratch that's not too complicated and well-commented. I am also keen to improve the bot and would be happy to take contributions to the code for general improvements or additional functionality.

I've tried my best to comment out as many lines as possible for easy comprehension and those not familiar with Discord.py. However, basic OOP knowledge is assumed.

There is some specific references to my guild still within the code, including our question list to new applicants. Please make sure to change these to suit your guild.

If you have any issues or concerns, please don't hesiate to reach out.

Thanks!

# Features
* Formatted Welcome Message
	* Automatic upon new server joiner
* Questionairre-style Application
	* Requires the command **!ApplyToJoin** to be issued by the applicant 
* Approve application
	* Requires the command **!Accept {UserID}** to be issed by a server admin with permissions to manage roles


# How to implement
If you'd like to just deploy and use this bot on your server, feel free! I've outlined the steps below for those who are new to Discord Bots

If you're not keen on coding and hosting it yourself, let me know. If I get enough demand, I can make this integratable to multiple servers and host it for you.

## Short version
* Set up & Install Python on your machine
* Download the Repo
* Configure
	* Change the variables in .env
	* Change the guild-specific variables in the code (public channel, application posting channel)
	* Change the function-specific variables in the code (questions to be asked, welcome message, doge picture)
* Run Main.py
* Test

## Long Version
* TBC :-)

# To-Do
All the awesome things I've love to keep working on this bot on. Pull requests welcome! But please comment and test them well.
## Improve Existing Features (code and funtion)
* Application
	* Only allow applicants to start this process with a DM command. The bot currently accepts this command from all channels it has access to
	* Check to see if the applicant already has member-specific roles to prevent internal spam
	* Check to see if the applicant has already submitted an application recently to prevent external spam. Maybe by checking through the submission channel and seeing if their UserID comes up?
	* Migrate the question list out of the main code body into some sort of structured environment variable, perhaps a JSON?
	* (Hard) - Only ask certain questions based off the response from another question (e.g. don't ask raider-level questions if the person only wants to be a social)
* Accept Application
	* Include a step that gives the result to the applicant (you've been accepted), and confirms if the applicant wants to join the guild. Maybe a message with a tick/cross emoji response for them to use?
	* Include personal notes from officers in the response (e.g. !Accept User456 'What a great application, we'd love an extra tank!')
* Error handling
	* Use Discord.Py's Bot error handling flow and migrate error handling logic out of the commands themselves
	* Log errors to the .log file and post errors in the officer application channel

## Add New Features
* Decline application
	* Template response with a polite message 
	* With personalised note for reason for declining
* Schedule Reminder
	* Notify server with @ Roles (Raiders, Members, Officers) on a weekly basis with events 15 mins before they start 
* Multi-guild compatiability
	* Allow bot to be setup for multiple guilds, with multiple question sets for different guilds
	* Ability to setup up bot (including questions and welcome message) using Discord instead of requiring code access