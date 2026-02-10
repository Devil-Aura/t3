import time
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import (
    add_admin, del_admin, get_admins, is_admin, 
    total_users_count, total_channels_count, total_links_count
)
from config import OWNER_ID
from plugins.helper_func import get_readable_time

@Client.on_message(filters.command("admins") & filters.user(OWNER_ID))
async def admin_list_handler(client, message):
    await show_admin_page(client, message, 0)

async def show_admin_page(client, message_or_query, page):
    admins = await get_admins()
    # Pagination Logic (5 per page)
    CHUNK_SIZE = 5
    start = page * CHUNK_SIZE
    end = start + CHUNK_SIZE
    current_admins = admins[start:end]
    
    buttons = []
    for adm in current_admins:
        buttons.append([InlineKeyboardButton(f"👤 {adm.get('name', 'Admin')}", callback_data=f"view_admin_{adm['id']}")])
    
    nav_btns = []
    if page > 0:
        nav_btns.append(InlineKeyboardButton("⬅️", callback_data=f"admins_page_{page-1}"))
    nav_btns.append(InlineKeyboardButton("➕ Add Admin", callback_data="add_admin_prompt"))
    if end < len(admins):
        nav_btns.append(InlineKeyboardButton("➡️", callback_data=f"admins_page_{page+1}"))
    
    buttons.append(nav_btns)
    
    text = "👮‍♂️ **Admin Management System**"
    
    if isinstance(message_or_query, CallbackQuery):
        await message_or_query.message.edit(text, reply_markup=InlineKeyboardMarkup(buttons))
    else:
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(buttons))

@Client.on_callback_query(filters.regex(r"^view_admin_(\d+)"))
async def view_admin_callback(client, query):
    if query.from_user.id != OWNER_ID: return
    user_id = int(query.data.split("_")[2])
    
    try:
        user = await client.get_users(user_id)
        info = f"Name: {user.first_name}\nID: {user.id}\nUsername: @{user.username}"
    except:
        info = f"ID: {user_id}\n(User not found by bot)"
        
    btns = [
        [InlineKeyboardButton("❌ Remove Admin", callback_data=f"del_admin_{user_id}")],
        [InlineKeyboardButton("🔙 Back", callback_data="admins_page_0")]
    ]
    await query.message.edit(info, reply_markup=InlineKeyboardMarkup(btns))

@Client.on_callback_query(filters.regex(r"^del_admin_(\d+)"))
async def delete_admin_callback(client, query):
    user_id = int(query.data.split("_")[2])
    await del_admin(user_id)
    await query.answer("Admin Removed!")
    await show_admin_page(client, query, 0)

@Client.on_callback_query(filters.regex("add_admin_prompt"))
async def add_admin_prompt(client, query):
    await query.message.reply("Send the User ID to add as admin:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cancel", callback_data="close_msg")]]))

@Client.on_message(filters.command("addadmin") & filters.user(OWNER_ID))
async def add_admin_cmd(client, message):
    try:
        uid = int(message.command[1])
        try:
            u = await client.get_users(uid)
            name = u.first_name
        except:
            name = "Unknown"
        await add_admin(uid, name)
        await message.reply(f"✅ Successfully added as admin: {name} ({uid})")
    except:
        await message.reply("Usage: /addadmin [user_id]")

# --- Stats & Status ---
@Client.on_message(filters.command("stats"))
async def stats_cmd(client, message):
    if not await is_admin(message.from_user.id): return
    u = await total_users_count()
    c = await total_channels_count()
    l = await total_links_count()
    await message.reply(f"📊 **Stats**\n\nUsers: {u}\nChannels: {c}\nLinks Created: {l}")

@Client.on_message(filters.command("ping"))
async def ping_cmd(client, message):
    s = time.time()
    m = await message.reply("Pong!")
    e = time.time()
    await m.edit(f"🏓 Pong! {round((e-s)*1000)}ms")

@Client.on_message(filters.command("status"))
async def status_cmd(client, message):
    if not await is_admin(message.from_user.id): return
    uptime = get_readable_time((datetime.now() - client.uptime).seconds)
    await message.reply(
        f"⚙️ sʏsᴛᴇᴍ sᴛᴀᴛᴜs\n\n"
        f"⏱ ᴜᴘᴛɪᴍᴇ: {uptime}\n"
        f"🕒 sᴛᴀʀᴛᴇᴅ: {client.uptime_str}\n"
    )
