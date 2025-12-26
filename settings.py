from main import bot
from database import disabled
from utils import is_admin

@bot.message_handler(commands=["disable"])
def disable_cmd(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        cmd = m.text.split()[1]
        disabled.add(cmd)
        bot.reply_to(m, f"⚠️ Command /{cmd} disabled.")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /disable <command>")

@bot.message_handler(commands=["enable"])
def enable_cmd(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        cmd = m.text.split()[1]
        disabled.discard(cmd)
        bot.reply_to(m, f"✅ Command /{cmd} enabled.")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /enable <command>")

@bot.message_handler(commands=["disabled"])
def show_disabled(m):
    if not disabled:
        bot.reply_to(m, "✅ No commands disabled.")
    else:
        bot.reply_to(m, "⚠️ Disabled commands:\n" + "\n".join(disabled))