from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import add_channel, remove_channel, get_all_channels, get_channel_by_name, is_admin
from config import OWNER_ID

@Client.on_message(filters.command("addchannel"))
async def add_channel_cmd(client, message):
    if not await is_admin(message.from_user.id): return
    
    # Usage: /addchannel [Anime Name] [Channel Id]
    try:
        args = message.text.split(maxsplit=2)
        name = args[1]
        ch_id = int(args[2])
    except:
        return await message.reply("Usage: `/addchannel [Anime Name] [Channel Id]`")
    
    try:
        # Check permissions
        member = await client.get_chat_member(ch_id, "me")
        if not member.privileges.can_invite_users:
            return await message.reply("❌ I don't have 'Invite Users via Link' permission in that channel.")
        
        # Generate Primary Link (Permanent)
        primary = await client.export_chat_invite_link(ch_id)
        
        await add_channel(name, ch_id, primary)
        await message.reply(f"✅ Successfully Added Channel [{name}]\nPrimary Link: {primary}")
        
    except Exception as e:
        await message.reply(f"Error: {e}\nMake sure I am admin in the channel.")

@Client.on_message(filters.command("channels"))
async def list_channels(client, message):
    if not await is_admin(message.from_user.id): return
    await show_channels_page(client, message, 0)

async def show_channels_page(client, message_or_query, page):
    channels = await get_all_channels()
    CHUNK = 5
    start = page * CHUNK
    end = start + CHUNK
    curr = channels[start:end]
    
    text = "**📺 Channels List**\n\n"
    me = (await client.get_me()).username
    
    for c in curr:
        req_link = f"https://t.me/{me}?start=req_{c['channel_id']}"
        nor_link = f"https://t.me/{me}?start=nor_{c['channel_id']}"
        text += (
            f"**{c.get('name', 'Unknown')}**\n"
            f"Primary: {c.get('primary_link')}\n"
            f"[Request Link]({req_link}) | [Normal Link]({nor_link})\n\n"
        )
        
    btns = []
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"ch_page_{page-1}"))
    nav.append(InlineKeyboardButton("➕ Add", callback_data="add_ch_prompt"))
    nav.append(InlineKeyboardButton("❌ Close", callback_data="close_msg"))
    if end < len(channels): nav.append(InlineKeyboardButton("➡️", callback_data=f"ch_page_{page+1}"))
    btns.append(nav)
    
    if isinstance(message_or_query, CallbackQuery):
        await message_or_query.message.edit(text, reply_markup=InlineKeyboardMarkup(btns), disable_web_page_preview=True)
    else:
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(btns), disable_web_page_preview=True)

@Client.on_callback_query(filters.regex(r"^ch_page_(\d+)"))
async def ch_pagination(client, query):
    page = int(query.data.split("_")[2])
    await show_channels_page(client, query, page)

@Client.on_message(filters.command("search"))
async def search_cmd(client, message):
    try:
        query = message.text.split(maxsplit=1)[1]
    except:
        return await message.reply("Usage: `/search [Anime Name]`")
        
    results = await get_channel_by_name(query)
    if not results:
        return await message.reply("No results found 🔎")
        
    text = "Here Are Some Search Results 🔎"
    btns = []
    for r in results:
        btns.append([InlineKeyboardButton(r['name'], callback_data=f"view_ch_{r['channel_id']}")])
        
    await message.reply(text, reply_markup=InlineKeyboardMarkup(btns))

@Client.on_callback_query(filters.regex(r"^view_ch_(-?\d+)"))
async def view_channel_detail(client, query):
    cid = int(query.data.split("_")[2])
    # Fetch detail logic here similar to list
    # For brevity, showing basic logic
    me = (await client.get_me()).username
    req = f"https://t.me/{me}?start=req_{cid}"
    nor = f"https://t.me/{me}?start=nor_{cid}"
    await query.message.reply(f"Links for {cid}:\nRequest: {req}\nNormal: {nor}")
