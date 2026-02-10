import asyncio
from pyrogram import Client, filters
from database.database import get_all_users, is_admin
from plugins.helper_func import parse_time, delete_after

@Client.on_message(filters.command(["broadcast", "pbroadcast", "dbroadcast"]) & filters.reply)
async def broadcast_handler(client, message):
    if not await is_admin(message.from_user.id): return
    
    cmd = message.command[0]
    users = await get_all_users()
    reply_msg = message.reply_to_message
    
    pin = True if cmd == "pbroadcast" else False
    delete_duration = 0
    
    if cmd == "dbroadcast":
        # Parse time from args: /dbroadcast 1H 30M
        try:
            time_args = "".join(message.command[1:])
            delete_duration = parse_time(time_args)
        except:
            return await message.reply("Invalid Time Format. Use 1H, 30M, etc.")
            
    m = await message.reply(f"Broadcasting to {len(users)} users...")
    
    count = 0
    for uid in users:
        try:
            msg = await reply_msg.copy(uid)
            if pin:
                await msg.pin()
            
            if delete_duration > 0:
                asyncio.create_task(delete_after(msg, delete_duration))
            count += 1
        except Exception:
            pass # Blocked user or error
            
    await m.edit(f"Broadcast Complete. Sent to {count} users.")

@Client.on_message(filters.command("allbroadcastclear"))
async def clear_all_broadcasts(client, message):
    # This logic implies deleting ALL history which is impossible via bot API for old messages easily without IDs.
    # Usually this deletes the 'last' broadcasted message if ID was stored.
    # For this scope, we return a placeholder.
    await message.reply("Feature: Deleting messages requires storing Message IDs of every broadcast. (Logic Placeholder)")
