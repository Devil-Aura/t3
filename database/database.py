import motor.motor_asyncio
import asyncio
from config import DB_URI, DB_NAME, OWNER_ID

client = motor.motor_asyncio.AsyncIOMotorClient(DB_URI)
db = client[DB_NAME]

# Collections
col_users = db['users']
col_channels = db['channels']
col_settings = db['settings']
col_admins = db['admins']
col_broadcast = db['broadcast_state']

# --- Users ---
async def add_user(user_id: int):
    await col_users.update_one({'_id': user_id}, {'$set': {'_id': user_id}}, upsert=True)

async def get_all_users():
    return [doc['_id'] async for doc in col_users.find({})]

async def get_stats():
    users = await col_users.count_documents({})
    channels = await col_channels.count_documents({})
    links = await col_channels.count_documents({}) * 3 # approx
    return users, channels, links

# --- Admins ---
async def add_admin_db(user_id: int):
    await col_admins.update_one({'_id': user_id}, {'$set': {'_id': user_id}}, upsert=True)

async def del_admin_db(user_id: int):
    await col_admins.delete_one({'_id': user_id})

async def get_admins_list():
    admins = [doc['_id'] async for doc in col_admins.find({})]
    return admins

# --- Channels ---
async def add_channel_db(anime_name, channel_id, primary_link):
    await col_channels.update_one(
        {'channel_id': channel_id},
        {'$set': {
            'anime_name': anime_name,
            'channel_id': channel_id,
            'primary_link': primary_link,
            'search_name': anime_name.lower()
        }},
        upsert=True
    )

async def del_channel_db(channel_id):
    await col_channels.delete_one({'channel_id': channel_id})

async def get_channel_by_name(name):
    return await col_channels.find_one({'search_name': {'$regex': name.lower()}})

async def get_channel_by_id(channel_id):
    return await col_channels.find_one({'channel_id': channel_id})

async def get_all_channels():
    return col_channels.find({})

async def search_channels_db(query):
    return col_channels.find({'search_name': {'$regex': query.lower()}})

# --- Settings (Customization) ---
async def set_setting(key, value):
    await col_settings.update_one({'key': key}, {'$set': {'value': value}}, upsert=True)

async def get_setting(key, default=None):
    doc = await col_settings.find_one({'key': key})
    return doc['value'] if doc else default

# Defaults
async def init_settings():
    # Set defaults if not exist
    if not await get_setting('caption'):
        await set_setting('caption', "Please Join The Channel By Clicking The Link Or Button And This Link Will Expire within few minutes.")
    if not await get_setting('button_text'):
        await set_setting('button_text', "⛩️ 𝗖𝗟𝗜𝗖𝗞 𝗛𝗘𝗥𝗘 𝗧𝗢 𝗝𝗢𝗜𝗇 ⛩️")
    if not await get_setting('revoke_time'):
        await set_setting('revoke_time', 1800) # 30 mins
    if not await get_setting('fsub_msg'):
        await set_setting('fsub_msg', "<b>ʀᴏᴋᴏ {first}!</b>\n\n<b>ᴛᴜᴍɴᴇ ᴀʙʜɪ ᴛᴀᴋ ʜᴀᴍᴀʀᴀ ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ ɴᴀʜɪɴ ᴋɪʏᴀ ʜᴀɪ!</b>\n<b><blockquote>ᴀɴɪᴍᴇ ᴋᴇ ᴇᴘɪꜱᴏᴅᴇꜱ ᴀᴜʀ ᴘᴜʀᴇ ᴀɴɪᴍᴇꜱ ʜɪɴᴅɪ ᴍᴇɪɴ ᴅᴇᴋʜɴᴇ ᴋᴇ ʟɪʏᴇ, ᴘᴇʜʟᴇ ʜᴀᴍᴀʀᴇ ᴄʜᴀɴɴᴇʟꜱ ᴊᴏɪɴ ᴋᴀʀɴᴀ ʜᴏɢᴀ।</b>\n<b>ꜱᴀʙ ᴄʜᴀɴɴᴇʟꜱ ᴊᴏɪɴ ᴋᴀʀɴᴇ ᴋᴇ ʙᴀᴀᴅ /start ʟɪᴋʜᴏ ᴀᴜʀ ᴍᴀᴢᴀ ʟᴜᴛᴏ!<blockquote>")
