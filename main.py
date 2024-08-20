from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, CallbackContext, CallbackQueryHandler
import json
import os

# Your bot token
TOKEN = '7409190990:AAEFfj5owT8zuT-Yu9u0uFzKsL8N2ixq4e0'

# Path to the file where channel IDs will be stored
CHANNELS_FILE = 'channels.json'

# Load channel IDs from file
def load_channel_ids():
    if os.path.exists(CHANNELS_FILE):
        with open(CHANNELS_FILE, 'r') as file:
            return json.load(file)
    return []

# Save channel IDs to file
def save_channel_ids(channel_ids):
    with open(CHANNELS_FILE, 'w') as file:
        json.dump(channel_ids, file)

# Initialize channel IDs
CHANNEL_IDS = load_channel_ids()

# Function to forward message to multiple channels
async def forward_message(update: Update, context: CallbackContext):
    message = update.message

    for channel_id in CHANNEL_IDS:
        try:
            if message.text:
                await context.bot.forward_message(chat_id=channel_id, from_chat_id=message.chat_id, message_id=message.message_id)
            elif message.photo:
                await context.bot.send_photo(chat_id=channel_id, photo=message.photo[-1].file_id, caption=message.caption)
            elif message.video:
                await context.bot.send_video(chat_id=channel_id, video=message.video.file_id, caption=message.caption)
            elif message.document:
                await context.bot.send_document(chat_id=channel_id, document=message.document.file_id, caption=message.caption)
            elif message.audio:
                await context.bot.send_audio(chat_id=channel_id, audio=message.audio.file_id, caption=message.caption)
            elif message.voice:
                await context.bot.send_voice(chat_id=channel_id, voice=message.voice.file_id, caption=message.caption)
            elif message.sticker:
                await context.bot.send_sticker(chat_id=channel_id, sticker=message.sticker.file_id)
            elif message.animation:
                await context.bot.send_animation(chat_id=channel_id, animation=message.animation.file_id, caption=message.caption)
            elif message.video_note:
                await context.bot.send_video_note(chat_id=channel_id, video_note=message.video_note.file_id)
        except Exception as e:
            print(f"Failed to forward message to {channel_id}: {e}")

# Command to start the bot
async def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Add Channel", callback_data='add')],
        [InlineKeyboardButton("Remove Channel", callback_data='remove')],
        [InlineKeyboardButton("List Channels", callback_data='list')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text('Choose an option:', reply_markup=reply_markup)

# Command to add a channel ID
async def add_channel(update: Update, context: CallbackContext):
    if context.args:
        channel_id = context.args[0]
        if channel_id not in CHANNEL_IDS:
            CHANNEL_IDS.append(channel_id)
            save_channel_ids(CHANNEL_IDS)
            await update.message.reply_text(f'Channel ID {channel_id} added.')
        else:
            await update.message.reply_text(f'Channel ID {channel_id} is already in the list.')
    else:
        await update.message.reply_text('Please provide a channel ID. For example: /add_channel -1001234567890')

# Command to remove a channel ID
async def remove_channel(update: Update, context: CallbackContext):
    if context.args:
        channel_id = context.args[0]
        if channel_id in CHANNEL_IDS:
            CHANNEL_IDS.remove(channel_id)
            save_channel_ids(CHANNEL_IDS)
            await update.message.reply_text(f'Channel ID {channel_id} removed.')
        else:
            await update.message.reply_text(f'Channel ID {channel_id} not found.')
    else:
        await update.message.reply_text('Please provide a channel ID. For example: /remove_channel -1001234567890')

# Command to list all channel IDs
async def list_channels(update: Update, context: CallbackContext):
    if CHANNEL_IDS:
        channels_list = "\n".join(CHANNEL_IDS)
        await update.message.reply_text(f"Added Channels:\n{channels_list}")
    else:
        await update.message.reply_text('No channels added yet.')

# Handle the callback queries for menu options
async def button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()

    if query.data == 'add':
        await add_channel(query, context)
    elif query.data == 'remove':
        await remove_channel(query, context)
    elif query.data == 'list':
        await list_channels(query, context)

def main():
    # Create application
    app = ApplicationBuilder().token(TOKEN).build()

    # Add command and message handlers
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('add_channel', add_channel))
    app.add_handler(CommandHandler('remove_channel', remove_channel))
    app.add_handler(CommandHandler('list_channels', list_channels))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, forward_message))

    # Start the bot
    app.run_polling()

if __name__ == '__main__':
    main()
