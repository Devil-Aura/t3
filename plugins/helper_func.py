import time
from datetime import datetime, timedelta
import asyncio

def get_readable_time(seconds: int) -> str:
    count = 0
    time_list = []
    time_suffix_list = ["s", "m", "h", "days"]
    while count < 4:
        count += 1
        remainder, result = divmod(seconds, 60) if count < 3 else divmod(seconds, 24)
        if seconds == 0 and remainder == 0:
            break
        time_list.append(int(result))
        seconds = int(remainder)
    
    for x in range(len(time_list)):
        time_list[x] = str(time_list[x]) + time_suffix_list[x]
    if len(time_list) == 4:
        time_list[-1] = time_list[-1] 
    
    time_list.reverse()
    return ":".join(time_list)

def parse_time(time_str):
    # Formats: 1H, 30M, 30s
    unit = time_str[-1].upper()
    value = int(time_str[:-1])
    if unit == 'H': return value * 3600
    if unit == 'M': return value * 60
    if unit == 'S': return value
    if unit == 'D': return value * 86400
    return 0

def get_bot_age():
    start_date = datetime(2026, 1, 26)
    now = datetime.now()
    delta = now - start_date
    return f"{delta.days} Days"

async def delete_after(message, delay):
    await asyncio.sleep(delay)
    try:
        await message.delete()
    except:
        pass
