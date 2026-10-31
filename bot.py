import os
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Aapke credentials
API_ID = 36174470
API_HASH = "ca51066771f3e8c48bf4904b9b122b29"
BOT_TOKEN = "8743877138:AAEFo-w4MDC4QJ7_TDHDpBPd0U0-GJJMQ7k"

app = Client(
    "video_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# Force Join Channels
FORCE_CHANNELS = ["@msti08", "@backup758"]

# Ads Link
ADS_LINK = "https://auctionr.org/4/89804def40749da824ad1835e422099f"

# Aapka Private Channel aur Video Message ID (Jo abhi aapne nikala hai)
PRIVATE_CHANNEL_ID = -1003979506532 
VIDEO_MESSAGE_ID = 3

@app.on_message(filters.command("start"))
async def start_handler(client, message):
    user_id = message.from_user.id
    
    not_joined_channels = []
    for channel in FORCE_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                not_joined_channels.append(channel)
        except Exception:
            not_joined_channels.append(channel)
            
    if not_joined_channels:
        buttons = []
        for ch in not_joined_channels:
            ch_name = ch.replace('@', '')
            buttons.append([InlineKeyboardButton(f"📢 Join {ch}", url=f"https://t.me/{ch_name}")])
        
        buttons.append([InlineKeyboardButton("🔄 Mainey Dono Channel Join Kar Liya", callback_data="check_join")])
        
        await message.reply(
            "⚠️ **Video paane ke liye pehle niche diye gaye sabhi channels ko join karein!**",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        return

    await send_ad_prompt(message)

async def send_ad_prompt(message):
    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("🔗 Ads Link (10 Second Rukein)", url=ADS_LINK)],
        [InlineKeyboardButton("✅ Video Prapt Karein", callback_data="get_video")]
    ])
    await message.reply(
        "✅ **Channels Verified!**\n\nAb niche diye gaye link par click karein, wahan website par **10 second** wait karein, aur wapas aakar **'Video Prapt Karein'** par click karein.",
        reply_markup=buttons
    )

@app.on_callback_query(filters.regex("check_join"))
async def check_join_callback(client, callback_query):
    user_id = callback_query.from_user.id
    not_joined = False
    for channel in FORCE_CHANNELS:
        try:
            member = await client.get_chat_member(channel, user_id)
            if member.status in ["left", "kicked"]:
                not_joined = True
        except Exception:
            not_joined = True
            
    if not_joined:
        await callback_query.answer("❌ Aapne abhi tak sabhi channels join nahi kiye hain!", show_alert=True)
    else:
        await callback_query.message.delete()
        await send_ad_prompt(callback_query.message)

@app.on_callback_query(filters.regex("get_video"))
async def get_video_callback(client, callback_query):
    await callback_query.message.delete()
    try:
        await client.copy_message(
            chat_id=callback_query.from_user.id,
            from_chat_id=PRIVATE_CHANNEL_ID,
            message_id=VIDEO_MESSAGE_ID
        )
    except Exception as e:
        await callback_query.message.reply(f"Video bhejte samay error aaya: {e}")

app.run()
