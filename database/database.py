import motor.motor_asyncio
from config import DATABASE_URL, DATABASE_NAME
from datetime import datetime

client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
db = client[DATABASE_NAME]

col_users = db.users
col_channels = db.channels
col_settings = db.settings
col_admins = db.admins
col_links = db.links

# --- Users ---
async def add_user(user_id):
    await col_users.update_one({'id': user_id}, {'$set': {'id': user_id}}, upsert=True)

async def get_all_users():
    return [x['id'] async for x in col_users.find({})]

async def total_users_count():
    return await col_users.count_documents({})

# --- Admins ---
async def add_admin(user_id, name):
    await col_admins.update_one({'id': user_id}, {'$set': {'id': user_id, 'name': name}}, upsert=True)

async def del_admin(user_id):
    await col_admins.delete_one({'id': user_id})

async def get_admins():
    return [x async for x in col_admins.find({})]

async def is_admin(user_id):
    from config import OWNER_ID
    if user_id == OWNER_ID: return True
    found = await col_admins.find_one({'id': user_id})
    return bool(found)

# --- Settings (Customization) ---
async def get_setting(key, default=None):
    doc = await col_settings.find_one({'type': 'config'})
    if not doc: return default
    return doc.get(key, default)

async def update_setting(key, value):
    await col_settings.update_one({'type': 'config'}, {'$set': {key: value}}, upsert=True)

# --- Channels ---
async def add_channel(anime_name, channel_id, primary_link):
    await col_channels.update_one(
        {'channel_id': channel_id},
        {'$set': {'channel_id': channel_id, 'name': anime_name, 'primary_link': primary_link}},
        upsert=True
    )

async def remove_channel(channel_id):
    await col_channels.delete_one({'channel_id': channel_id})

async def get_channel_by_name(name):
    # Regex search for similar names
    return [x async for x in col_channels.find({'name': {'$regex': name, '$options': 'i'}})]

async def get_all_channels():
    return [x async for x in col_channels.find({})]

async def total_channels_count():
    return await col_channels.count_documents({})

# --- Links ---
async def total_links_count():
    # This is just a counter logic, or count documents in links collection
    return await col_links.count_documents({})
