import discord
import os
import asyncio
from datetime import datetime, timezone

TOKEN = os.environ["TOKEN"]
USER_ID = int(os.environ["USER_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

alert_task = None

def seconds_until_next_restock():
    now = datetime.now(timezone.utc)

    # Restocks happen whenever the minute is divisible by 5
    seconds_into_hour = now.minute * 60 + now.second + now.microsecond / 1_000_000
    wait = 300 - (seconds_into_hour % 300)

    # If we're basically exactly on a restock time, send now
    if wait >= 299.9:
        wait = 0

    return wait

async def restock_loop():
    await client.wait_until_ready()

    while not client.is_closed():
        wait = seconds_until_next_restock()
        print(f"Waiting {wait:.1f} seconds until next restock")
        await asyncio.sleep(wait)

        user = await client.fetch_user(USER_ID)
        await user.send("🛒 Mini Wars shop restocked! Check for Mythical+.")

        # Wait a little so it doesn't send twice at the same :00/:05 time
        await asyncio.sleep(1)

@client.event
async def on_ready():
    global alert_task
    print(f"Logged in as {client.user}")

    if alert_task is None or alert_task.done():
        alert_task = asyncio.create_task(restock_loop())

client.run(TOKEN)
