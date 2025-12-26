from main import bot
from database import filters
from utils import is_admin

# ---------------- ADD FILTER ----------------
@bot.message_handler(commands=["filter"])
def add_filter(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        key = m.text.split()[1]
        value = " ".join(m.text.split()[2:])
        filters[key] = value
        bot.reply_to(m, f"✅ Filter added: {key}")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /filter <keyword> <reply>")

# ---------------- SHOW FILTERS ----------------
@bot.message_handler(commands=["filters"])
def show_filters(m):
    if not filters:
        bot.reply_to(m, "✅ No filters set.")
    else:
        text = "\n".join([f"{k} → {v}" for k, v in filters.items()])
        bot.reply_to(m, f"📝 Active Filters:\n{text}")

# ---------------- DELETE FILTER ----------------
@bot.message_handler(commands=["stop"])
def delete_filter(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        key = m.text.split()[1]
        if key in filters:
            filters.pop(key)
            bot.reply_to(m, f"✅ Filter removed: {key}")
        else:
            bot.reply_to(m, "⚠️ Filter not found")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /stop <keyword>")

# ---------------- FILTER REPLY ----------------
@bot.message_handler(func=lambda m: m.text in filters)
def reply_filter(m):
    bot.reply_to(m, filters[m.text])