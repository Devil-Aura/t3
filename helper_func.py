import asyncio
import time
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import OWNER_ID
from database.database import get_admins_list

async def is_admin(user_id):
    if user_id == OWNER_ID:
        return True
    admins = await get_admins_list()
    return user_id in admins

def get_readable_time(seconds):
    seconds = int(seconds)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{days}d {hours}h {minutes}m {seconds}s"

def parse_time(time_str):
    # Returns seconds
    time_str = time_str.lower()
    if 'd' in time_str:
        return int(time_str.replace('d', '')) * 86400
    elif 'h' in time_str:
        return int(time_str.replace('h', '')) * 3600
    elif 'm' in time_str:
        return int(time_str.replace('m', '')) * 60
    elif 's' in time_str:
        return int(time_str.replace('s', ''))
    else:
        try:
            return int(time_str)
        except:
            return 0

async def delete_after(message, seconds):
    await asyncio.sleep(seconds)
    try:
        await message.delete()
    except:
        pass

def get_age():
    from datetime import datetime
    start_date = datetime(2026, 1, 26)
    now = datetime.now()
    delta = now - start_date
    return f"{delta.days} Days"
