# random code

## Table of Contents
- [Introduction](#introduction)
- [Instalation](#instalation)
- [Projects](#projects)
  - [Discord Bot](#discordbot)
  - [Shutdown PC](#shutdownpc)
- [change log](#changelog)
 
## Introduction

This repository is called "Random Code" because I write random python code, that I at that time think is nice to have.

## Instalation
Each sub-project has it's own folder, in there you will find a requirements.txt that will install the required modules with this command: `pip install -r requirements.txt`

## Projects
- [x] [Discord Bot](#discordbot)
- [x] [Shutdown PC](#shutdownpc)

### DiscordBot
This is a discord bot that I created because sometimes I'm too lazy to get out of my bed to turn off my pc. So I created this code that runs as a discord bot, so I can turn it off via a discord command. I can also open teamviewer and let it send me a screenshot of the login info. Also you can set a timer with the `!shutdownIn` or `!shutdownAt` command. The `!shutdownIn` commands is a good command for example you want to listen to some music while you are faling asleep, you can do `!shutdownIn 2h` which makes your PC shut down in 2 hours. The `!shutdownAt` command is a bit different since it works with time. Ex. `!shutdownAt 11pm` will shut down your PC when the your local time is 11pm.

### ShutdownPC
This is a simple script that shuts down your PC after a certain amount of time. This code only has the function `!shutdownIn` as discribed in the [DiscordBot](#discordbot). And this code works in a commandline, like cmd, the terminal of visual studio code, etc.

## Changelog
You can find the changelog [here](https://github.com/HowlingArcher/random-code/blob/main/changeLog.md)