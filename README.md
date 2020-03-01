# Slackbot

This project is a small prototype of a python Slackbot, architectured to easily add new instructions.

Adding a new command is as simple as:

 * Adding a new folder in `internal/cmd`
 * Registering the command in CommandsRegistry 

On a new message, slack bot will check a few parameters, match the message with registered commands' regex and then answer with an intent message: a message describing what the bot is going to do.
User can then approve the intent by adding a tick reaction to the message.

This 2 steps procedure helps reducing mistakes in case of overlapping regex.
