from main import bot
from telebot.types import ChatPermissions
from database import flood
from utils import is_admin
from datetime import datetime, timedelta

# Set the limits
MAX_MESSAGES = 5          # Max messages allowed
TIME_FRAME = 10           # Time frame in seconds
MUTE_TIME = 30            # Mute time in seconds

@bot.message_handler(func=lambda m: True, content_types=['text', 'sticker', 'photo', 'video'])
def anti_flood(m):
    user_id = m.from_user.id
    chat_id = m.chat.id

    # Skip admins
    if is_admin(bot, chat_id, user_id):
        return

    now = datetime.now()

    # Initialize user data
    if user_id not in flood:
        flood[user_id] = []

    # Add current message time
    flood[user_id].append(now)

    # Remove messages older than TIME_FRAME
    flood[user_id] = [t for t in flood[user_id] if (now - t).total_seconds() <= TIME_FRAME]

    # Check if user exceeded limit
    if len(flood[user_id]) > MAX_MESSAGES:
        try:
            # Mute user temporarily
            until = now + timedelta(seconds=MUTE_TIME)
            bot.restrict_chat_member(
                chat_id,
                user_id,
                until_date=until,
                permissions=ChatPermissions(can_send_messages=False)
            )
            bot.send_message(chat_id, f"⚠️ User [{m.from_user.first_name}](tg://user?id={user_id}) muted for spamming ({MUTE_TIME} sec)")
            # Clear the list after mute
            flood[user_id] = []
        except Exception as e:
            print(f"Error muting user: {e}")