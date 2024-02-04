import discord
from discord.ext import commands
import os
import sys
import asyncio
from datetime import datetime, timedelta
import subprocess
import pyautogui

# Define intents
intents = discord.Intents.default()
intents.messages = True  # Enable the 'messages' intent
intents.message_content = True  # Enable the 'message content' intent

# Create an instance of the bot with intents
bot = commands.Bot(command_prefix='!', intents=intents)

# Event: Bot is ready
@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.offline)
    print(f'Logged in as {bot.user.name} ({bot.user.id})')

# Command: !shutdown
@bot.command(name='shutdown', help='Shuts down the PC')
async def shutdown_cmd(ctx):
    await ctx.send('Shutting Down PC...')
    # wait 2 seconds
    await asyncio.sleep(2)
    # shut down the pc
    await pc_shutdown()

# Command: !restart
@bot.command(name='restart', help='Restarts the PC')
async def shutdown_cmd(ctx):
    await ctx.send('Restarting PC...')
    # wait 2 seconds
    await asyncio.sleep(2)
    # shut down the pc
    await pc_restart()

@bot.command(name='update', help="Shuts down PC after installing an update")
async def update(ctx):
    await ctx.send("Shutting PC down after update...")
    # wait 2 seconds
    await asyncio.sleep(2)
    # trigger the function
    await pc_update_shutdown()

shutdowns = {}

# Function to update shutdown timer
async def update_shutdown_timer(ctx, end_time):
    while datetime.utcnow() < end_time:
        remaining_time = end_time - datetime.utcnow()
        minutes, seconds = divmod(remaining_time.seconds, 60)
        await ctx.send(f"Time remaining: {minutes} minutes, {seconds} seconds")
        await asyncio.sleep(60)  # Wait for 1 minute

    await ctx.send("Shutting down PC!")
    await asyncio.sleep(2)
    await pc_shutdown()

@bot.command(name='shutdownIn', help='Start a shutdown timer')
async def start_shutdown(ctx, time_input):
    try:
        # Parse the time input
        time_delta = timedelta()
        for part in time_input.split():
            if part[-1] == 'h':
                time_delta += timedelta(hours=int(part[:-1]))
            elif part[-1] == 'm':
                time_delta += timedelta(minutes=int(part[:-1]))
            elif part[-1] == 's':
                time_delta += timedelta(seconds=int(part[:-1]))

        # Calculate end time
        end_time = datetime.utcnow() + time_delta

        # Start the shutdown timer
        shutdowns[ctx.author.id] = asyncio.create_task(update_shutdown_timer(ctx, end_time))

    except ValueError:
        await ctx.send("Invalid time format. Please use 'h' for hours, 'm' for minutes, 's' for seconds")

# Command: !cancelshutdown
@bot.command(name='cancelshutdown', help='Cancel the active shutdown')
async def cancel_shutdown(ctx):
    if ctx.author.id in shutdowns:
        shutdowns[ctx.author.id].cancel()
        await ctx.send("shutdown canceled.")
    else:
        await ctx.send("No active shutdown to cancel.")

@bot.command(name='shutdownAt')
async def remind(ctx, time_str):
    try:
        time = datetime.strptime(time_str, '%I%p').time()
    except ValueError:
        await ctx.send('Invalid time format. Please use HH:MMam/pm.')
        return

    now = datetime.now().time()
    remind_time = datetime.combine(datetime.today(), time)

    if now > time:
        remind_time += timedelta(days=1)  # If the time has already passed, schedule for the next day

    time_until_shutdown = (remind_time - datetime.now()).total_seconds()
    await ctx.send(f'Shutdown at {time_str}\nThere is no way to cancel this xD')
    # Schedule the shutdown
    await asyncio.sleep(time_until_shutdown)
    await ctx.send(f'Shutting down PC...')
    await asyncio.sleep(2)
    await pc_shutdown()

@bot.command(name='teamviewer')
async def remind(ctx):
    await ctx.send(f'Opening TeamViewer')
    await open_teamviewer(ctx)

# open the application "teamviewer"
async def open_teamviewer(ctx):
    # Replace the path with the actual path to your teamvieuwer executable
    TeamViewer_path = r'C:\Program Files\TeamViewer\TeamViewer.exe'

    try:
        subprocess.Popen([TeamViewer_path])
        print("Teamviewer is opening...")
        await asyncio.sleep(10)
        await take_screenshot(ctx)
    except Exception as e:
        print(f"Error: {e}")

async def take_screenshot(ctx):
    # Take a screenshot
    screenshot = pyautogui.screenshot()

    # Save the screenshot
    screenshot.save("screenshot.png")

    print("Screenshot saved.")

    await asyncio.sleep(10)
    # send the screenshot.png in discord
    await send_screenshot(ctx)

async def send_screenshot(ctx):
    # send the screenshot.png in discord
    await ctx.send(file=discord.File('screenshot.png'))

async def pc_shutdown():
    # shut down the pc running this code:
    os.system("shutdown /s /t 1")
    sys.exit()

async def pc_restart():
    # restart the pc running this code:
    os.system("shutdown /r /t 1")

async def pc_update_shutdown():
    # shuts down pc after an update is installed:
    os.system("wuauclt /detectnow /updatenow && shutdown /s /t 0")
    sys.exit()

# Run the bot with your token
bot.run('YOUR_DISCORD_TOKEN')
