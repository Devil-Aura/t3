import asyncio
from pyrogram import Client, filters, enums
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from config import OWNER_ID
from database.database import add_user, get_setting, get_all_channels
from plugins.helper_func import get_bot_age, delete_after, parse_time

# --- Constants & Defaults ---
DEFAULT_REVOKE_TIME = 1800 # 30 mins
DEFAULT_DELETE_TIME = 1800 # 30 mins

@Client.on_message(filters.command("start"))
async def start_handler(client, message):
    await add_user(message.from_user.id)
    
    # Check if maintenance mode is on
    maint_mode = await get_setting("maintenance", False)
    if maint_mode and message.from_user.id != OWNER_ID:
        return await message.reply("⚠️ The Bot Is Under Maintenance. After Few Time Bot Will Back To Work.")

    text = message.text
    if len(text.split()) > 1:
        # Handle Link Logic (Token)
        token = text.split()[1]
        await handle_link_access(client, message, token)
        return

    # Normal Start Message
    msg_text = (
        "Konnichiwa! 🤗\n"
        "Mera Naam **Crunchyroll Link Provider** hai.\n\n"
        "Main aapko **anime channels** ki links provide karta hu, Iss Anime Ke Channel Se.\n\n"
        "<blockquote>"
        "🔹 Agar aapko kisi anime ki link chahiye,<br>"
        "🔹 Ya channel ki link nahi mil rahi hai,<br>"
        "🔹 Ya link expired ho gayi hai"
        "</blockquote>\n"
        "Toh aap **@CrunchyRollChannel** se New aur working links le sakte hain.\n\n"
        "Shukriya! ❤️"
    )
    
    m = await message.reply(msg_text)
    # Delete after 15 minutes (900 seconds)
    asyncio.create_task(delete_after(m, 900))

@Client.on_message(filters.command("help"))
async def help_handler(client, message):
    txt = (
        "<blockquote expandable>"
        " **🆘 Help & Support**\n"
        " Agar aapko kisi bhi help ki zaroorat hai, toh humse yahan sampark karein:\n"
        "**@CrunchyRollHelper**"
        "</blockquote>\n\n"
        "**🎬 More Anime**\n"
        "Agar aap aur anime dekna chahte hain, toh yahan se dekh sakte hain:\n"
        "**@CrunchyRollChannel**\n\n"
        "<blockquote expandable>"
        "**🤖 Bot Info**\n"
        "Bot ki jaankari ke liye /about ya /info ka istemal karein."
        "</blockquote>"
    )
    m = await message.reply(txt)
    # Delete after 2 mins (120s)
    asyncio.create_task(delete_after(m, 120))

@Client.on_message(filters.command(["about", "info"]))
async def about_handler(client, message):
    age = get_bot_age()
    txt = (
        "About The Bot\n"
        "🤖 My Name :- <a href='https://telegra.ph/Crunchy-Roll-Vault-04-08'>Crunchyroll Link Provider</a>\n"
        f"Bot Age :- {age} (26/01/2026)\n"
        "Anime Channel :- <a href='https://t.me/Crunchyrollchannel'>Crunchy Roll Channel</a>\n"
        "Language :- <a href='https://t.me/Crunchyrollchannel'>Python</a>\n"
        "Developer: :- <a href='https://t.me/World_Fastest_Bots'>World Fastest Bots</a>\n\n"
        "This Is Private/Paid Bot Provided By \n"
        "@World_Fastest_Bots."
    )
    
    btns = InlineKeyboardMarkup([
        [InlineKeyboardButton("📡 𝗣𝗼𝘄𝗲𝗿𝗲𝗱 𝗕𝘆", url="https://t.me/World_Fastest_Bots")],
        [InlineKeyboardButton("World Fastest Bots", url="https://t.me/World_Fastest_Bots")]
    ])
    
    m = await message.reply(txt, reply_markup=btns, disable_web_page_preview=True)
    # Delete after 1 min (60s)
    asyncio.create_task(delete_after(m, 60))

# --- Main Link Handling Logic ---
async def handle_link_access(client, message, token):
    try:
        # Token format: req_CHANNELID or nor_CHANNELID
        mode = "request" if token.startswith("req_") else "normal"
        channel_id = int(token.split("_")[1])
        
        # Get Revoke Time Setting
        revoke_seconds = await get_setting("revoke_time", DEFAULT_REVOKE_TIME)
        
        # Generate Link
        # Note: creates_join_request=True for Request Link
        is_req = True if mode == "request" else False
        
        # Create Invite Link (Revokable)
        invite = await client.create_chat_invite_link(
            chat_id=channel_id,
            name="Temp Link by Bot",
            expire_date=None, # We manually revoke or let python handle expiry if supported, user asked for manual revoke logic via bot
            creates_join_request=is_req
        )
        
        # Image Post
        img = await get_setting("custom_image", "https://telegra.ph/file/f3d3aff9ec422158feb05-d2180e3665e0ac4d32.jpg")
        caption = await get_setting("custom_caption", "Channel link 🔗 👇👇\n\n[link]\n[link]")
        btn_text = await get_setting("custom_btn_text", "⛩️ 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗝𝗢𝗜𝗇 ⛩️")
        
        final_caption = caption.replace("[link]", invite.invite_link)
        
        msg1 = await message.reply_photo(
            photo=img,
            caption=final_caption,
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(btn_text, url=invite.invite_link)]
            ])
        )
        
        msg2 = await msg1.reply(
            "Please Join The Channel By Clicking The Link Or Button And This Link Will Expire within few minutes."
        )
        
        # Auto Delete Messages
        del_time = await get_setting("delete_time", DEFAULT_DELETE_TIME)
        asyncio.create_task(delete_after(msg1, del_time))
        asyncio.create_task(delete_after(msg2, del_time))
        
        # Revoke Link Task
        asyncio.create_task(revoke_task(client, channel_id, invite.invite_link, revoke_seconds))
        
    except Exception as e:
        await message.reply(f"Error: {e}")

async def revoke_task(client, chat_id, link, delay):
    await asyncio.sleep(delay)
    try:
        await client.revoke_chat_invite_link(chat_id, link)
    except:
        pass
