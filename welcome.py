from main import bot
from database import welcome, goodbye
from utils import is_admin

# ---------------- SET WELCOME ----------------
@bot.message_handler(commands=["setwelcome"])
def set_welcome(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    global welcome
    welcome = m.text.replace("/setwelcome","").strip()
    bot.reply_to(m, "✅ Welcome message set.")

# ---------------- SHOW WELCOME ----------------
@bot.message_handler(commands=["welcome"])
def show_welcome(m):
    bot.reply_to(m, welcome or "No welcome message set.")

# ---------------- SET GOODBYE ----------------
@bot.message_handler(commands=["setgoodbye"])
def set_goodbye(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    global goodbye
    goodbye = m.text.replace("/setgoodbye","").strip()
    bot.reply_to(m, "✅ Goodbye message set.")

# ---------------- SHOW GOODBYE ----------------
@bot.message_handler(commands=["goodbye"])
def show_goodbye(m):
    bot.reply_to(m, goodbye or "No goodbye message set.")