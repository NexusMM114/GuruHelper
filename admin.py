from main import bot
from utils import is_admin
from database import warns
from datetime import datetime, timedelta
from telebot.types import ChatPermissions

@bot.message_handler(commands=["ban","kick"])
def ban(m):
    if is_admin(bot,m.chat.id,m.from_user.id) and m.reply_to_message:
        bot.kick_chat_member(m.chat.id, m.reply_to_message.from_user.id)
        bot.reply_to(m,"🚫 User banned")

@bot.message_handler(commands=["unban"])
def unban(m):
    if is_admin(bot,m.chat.id,m.from_user.id):
        bot.unban_chat_member(m.chat.id, int(m.text.split()[1]))
        bot.reply_to(m,"✅ User unbanned")

@bot.message_handler(commands=["mute","tmute","tempmute"])
def mute(m):
    if is_admin(bot,m.chat.id,m.from_user.id):
        until = datetime.now() + timedelta(minutes=10)
        bot.restrict_chat_member(
            m.chat.id,
            m.reply_to_message.from_user.id,
            until_date=until,
            permissions=ChatPermissions(can_send_messages=False)
        )
        bot.reply_to(m,"🔇 User muted (10 min)")

@bot.message_handler(commands=["unmute"])
def unmute(m):
    if is_admin(bot,m.chat.id,m.from_user.id):
        bot.restrict_chat_member(
            m.chat.id,
            m.reply_to_message.from_user.id,
            permissions=ChatPermissions(
                can_send_messages=True,
                can_send_media_messages=True,
                can_send_other_messages=True,
                can_add_web_page_previews=True
            )
        )
        bot.reply_to(m,"🔊 User unmuted")

@bot.message_handler(commands=["warn"])
def warn(m):
    if is_admin(bot,m.chat.id,m.from_user.id):
        uid = m.reply_to_message.from_user.id
        warns[uid] = warns.get(uid,0)+1
        if warns[uid]>=3:
            bot.kick_chat_member(m.chat.id,uid)
            bot.reply_to(m,"🚫 User banned (3 warns)")
        else:
            bot.reply_to(m,f"⚠️ Warning {warns[uid]}/3")

@bot.message_handler(commands=["warns","resetwarns","delwarns"])
def warn_tools(m):
    warns.clear()
    bot.reply_to(m,"♻️ All warns reset")