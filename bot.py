import asyncio
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
from datetime import datetime
import os

if not os.path.exists("plugins"):
    os.makedirs("plugins")

class LinkBot(Client):
    def __init__(self):
        super().__init__(
            "LinkShareBot",
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,
            plugins=dict(root="plugins")
        )
        self.uptime = datetime.now()
        self.uptime_str = self.uptime.strftime("%Y-%m-%d %H:%M:%S")

    async def start(self):
        await super().start()
        print("Bot Started! 🤖")
        print(f"Me: @{(await self.get_me()).username}")

    async def stop(self, *args):
        await super().stop()
        print("Bot Stopped.")

if __name__ == "__main__":
    LinkBot().run()
