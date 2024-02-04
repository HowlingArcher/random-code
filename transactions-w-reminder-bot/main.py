import json
from datetime import datetime
import discord
from discord.ext import commands, tasks

# Replace 'YOUR_DISCORD_TOKEN' with your actual Discord bot token
DISCORD_TOKEN = 'YOUR_DISCORD_TOKEN'

# Path to your JSON file
json_file_path = 'spending_tracker.json'

intents = discord.Intents.default()
intents.messages = True
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)

def load_data():
    try:
        with open(json_file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        data = {'withdrawals': [], 'earnings': []}
    return data

def save_data(data):
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=2)

def add_withdrawal(amount, date, reason):
    data = load_data()
    data['withdrawals'].append({'date': date, 'amount': amount, 'reason': reason})
    save_data(data)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    remind_task.start()

@tasks.loop(hours=24)
async def remind_task():
    data = load_data()
    today = datetime.today().strftime('%Y-%m-%d')

    if not any(withdrawal['date'] == today for withdrawal in data['withdrawals']):
        await send_reminder()

@bot.command(name='spend', help='Manually enter your spending with amount, date, and reason')
async def spending(ctx, amount: float, date: str, *, reason: str):
    try:
        datetime.strptime(date, '%m/%Y')
    except ValueError:
        await ctx.send("Invalid date format. Please use MM/YYYY.")
        return

    add_withdrawal(amount, date, reason)
    await ctx.send("withdrawal added successfully!")

@bot.command(name='lookup', help='Look up withdrawals and earnings in a specific month and year')
async def lookup(ctx, date: str):
    try:
        # Extracting month and year from the date
        month, year = map(int, date.split('/'))
        datetime.strptime(date, '%m/%Y')
    except (ValueError, IndexError):
        await ctx.send("Invalid date format. Please use MM/YYYY.")
        return

    data = load_data()

    withdrawals_in_month = [withdrawal for withdrawal in data['withdrawals'] if
                             datetime.strptime(withdrawal['date'], '%m/%Y').month == month and
                             datetime.strptime(withdrawal['date'], '%m/%Y').year == year]

    earnings_in_month = [earning for earning in data['earnings'] if
                         datetime.strptime(earning['date'], '%m/%Y').month == month and
                         datetime.strptime(earning['date'], '%m/%Y').year == year]

    total_spent = sum(withdrawal['amount'] for withdrawal in withdrawals_in_month)
    total_earned = sum(earning['amount'] for earning in earnings_in_month)

    remaining_balance = total_earned - total_spent

    response = f"withdrawals and Earnings in {month}/{year}:\n"
    
    if withdrawals_in_month:
        response += "withdrawals:\n"
        for withdrawal in withdrawals_in_month:
            response += f"{withdrawal['date']} - Amount: €{withdrawal['amount']}, Reason: {withdrawal['reason']}\n"

    if earnings_in_month:
        response += "Earnings:\n"
        for earning in earnings_in_month:
            response += f"{earning['date']} - Amount: €{earning['amount']}, Source: {earning['source']}\n\n"

    response += f"Total Amount Spent: €{total_spent}\n"
    response += f"Total Amount Earned: €{total_earned}\n"
    response += f"Remaining Balance: €{remaining_balance}"

    await ctx.send(response)


@bot.command(name='earn', help='Manually enter your earnings with amount, date, and source')
async def earn(ctx, amount: float, date: str, *, source: str):
    try:
        datetime.strptime(date, '%m/%Y')
    except ValueError:
        await ctx.send("Invalid date format. Please use MM/YYYY.")
        return

    add_earning(amount, date, source)
    await ctx.send("Earning added successfully!")

def add_earning(amount, date, source):
    data = load_data()
    data['earnings'].append({'date': date, 'amount': amount, 'source': source})
    save_data(data)


async def send_reminder():
    # Replace 'YOUR_CHANNEL_ID' with the actual channel ID where you want to send reminders
    channel_id = 'YOUR_CHANNEL_ID'
    channel = bot.get_channel(int(channel_id))
    await channel.send("Don't forget to track your spending today!")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN)
