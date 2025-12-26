import telebot
from config import TOKEN, BOT_NAME, BOT_TAGLINE

bot = telebot.TeleBot(TOKEN, parse_mode="Markdown")

import admin
import locks
import antiflood
import blacklist
import filters
import welcome
import rules
import info
import fun
import settings
import owner

print(f"🔐 {BOT_NAME} Running...")

@bot.message_handler(commands=["start"])
def start(m):
    bot.reply_to(
        m,
        f"🔐 *{BOT_NAME}*\n"
        f"{BOT_TAGLINE}\n\n"
        "Use /help to see all commands"
    )

@bot.message_handler(commands=["help"])
def help_cmd(m):
    bot.reply_to(
        m,
        f"🔐 *{BOT_NAME} Commands*\n\n"
        "Admin: /ban /unban /mute /unmute /warn /warns /delwarns /kick /promote /demote /adminlist /staff\n"
        "Locks: /lock /unlock /locktypes /lock media /lock links /lock bots /unlock\n"
        "Filters: /filter /filters /stop\n"
        "Blacklist: /blacklist /blacklists\n"
        "Welcome/Goodbye: /setwelcome /welcome /setgoodbye /goodbye\n"
        "Rules: /setrules /rules\n"
        "Info: /id /info /stats /ping /about\n"
        "Fun: /dice /roll /slap /hug /shrug /runs /tableflip\n"
        "Owner: /gban /broadcast /leave /restart"
    )

bot.infinity_polling()