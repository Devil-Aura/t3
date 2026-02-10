from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import is_admin, get_setting, update_setting
from plugins.helper_func import parse_time

@Client.on_message(filters.command("customize"))
async def customize_menu(client, message):
    if not await is_admin(message.from_user.id): return
    await show_main_menu(message)

async def show_main_menu(message_or_query):
    text = "Here you can customise all the things of bot."
    btns = [
        [InlineKeyboardButton("Image Post", callback_data="cust_image"), InlineKeyboardButton("Second Message", callback_data="cust_msg2")],
        [InlineKeyboardButton("Revoke Time", callback_data="cust_revoke"), InlineKeyboardButton("Force Sub", callback_data="cust_fsub")],
        [InlineKeyboardButton("Maintenance Mode", callback_data="cust_maint")],
        [InlineKeyboardButton("Close", callback_data="close_msg")]
    ]
    if isinstance(message_or_query, CallbackQuery):
        await message_or_query.message.edit(text, reply_markup=InlineKeyboardMarkup(btns))
    else:
        await message_or_query.reply(text, reply_markup=InlineKeyboardMarkup(btns))

@Client.on_callback_query(filters.regex(r"^cust_"))
async def customization_handler(client, query):
    data = query.data
    
    if data == "cust_image":
        text = "Here you can customise Image Post Message"
        btns = [
            [InlineKeyboardButton("Caption", callback_data="cust_caption"), InlineKeyboardButton("Image", callback_data="cust_img_set")],
            [InlineKeyboardButton("Button Text", callback_data="cust_btn_text")],
            [InlineKeyboardButton("Back", callback_data="cust_main"), InlineKeyboardButton("Close", callback_data="close_msg")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btns))

    elif data == "cust_caption":
        curr = await get_setting("custom_caption", "Default")
        await query.message.edit(
            f"Current Caption:\n{curr}\n\nSend new caption (Use [link] for link position).",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="cust_image")]])
        )
        # Add listener logic here (simplified for this code block: use /setcaption command or similar state)
        
    elif data == "cust_revoke":
        curr = await get_setting("revoke_time", 1800)
        text = f"The current revoke time is {curr} seconds.\nClick Set New Time to change."
        btns = [
            [InlineKeyboardButton("Set New Time", callback_data="set_revoke_time")],
            [InlineKeyboardButton("Back", callback_data="cust_main")]
        ]
        await query.message.edit(text, reply_markup=InlineKeyboardMarkup(btns))
        
    elif data == "cust_maint":
        curr = await get_setting("maintenance", False)
        status = "ON" if curr else "OFF"
        toggle = not curr
        await update_setting("maintenance", toggle)
        await query.answer(f"Maintenance Mode is now {not curr}")
        await show_main_menu(query)
    
    elif data == "cust_main":
        await show_main_menu(query)

# Note: For text inputs (Set Caption, Set Time), the best practice in Pyrogram is using client.listen 
# or a conversation handler state. Since I cannot provide a full conversation engine file here, 
# I recommend using commands for setting values or a simple `pyromod` listener.
