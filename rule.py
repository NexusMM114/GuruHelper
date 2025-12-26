from main import bot
from database import rules
from utils import is_admin

@bot.message_handler(commands=["setrules"])
def set_rules(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    global rules
    rules = m.text.replace("/setrules","").strip()
    bot.reply_to(m, "✅ Rules updated.")

@bot.message_handler(commands=["rules"])
def show_rules(m):
    bot.reply_to(m, rules or "No rules set.")