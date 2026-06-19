import discord
from discord.ext import tasks
import os

TOKEN = os.environ["TOKEN"]
USER_ID = int(os.environ["USER_ID"])

intents = discord.Intents.default()
client = discord.Client(intents=intents)

@tasks.loop(minutes=5)
async def restock():
    user = await client.fetch_user(USER_ID)
    await user.send("🛒 Mini Wars shop restocked!")

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")
    restock.start()

client.run(TOKEN)
