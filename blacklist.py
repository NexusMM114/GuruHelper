from main import bot
from database import blacklist
from utils import is_admin

# ---------------- ADD WORD TO BLACKLIST ----------------
@bot.message_handler(commands=["blacklist"])
def add_blacklist(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        word = m.text.split(maxsplit=1)[1].lower()
        blacklist.add(word)
        bot.reply_to(m, f"🚫 Word '{word}' added to blacklist.")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /blacklist <word>")

# ---------------- SHOW BLACKLIST ----------------
@bot.message_handler(commands=["blacklists"])
def show_blacklist(m):
    if not blacklist:
        bot.reply_to(m, "✅ No words in blacklist.")
    else:
        bot.reply_to(m, "🚫 Blacklisted words:\n" + "\n".join(blacklist))

# ---------------- REMOVE WORD FROM BLACKLIST ----------------
@bot.message_handler(commands=["unblacklist"])
def remove_blacklist(m):
    if not is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        word = m.text.split(maxsplit=1)[1].lower()
        if word in blacklist:
            blacklist.remove(word)
            bot.reply_to(m, f"✅ Word '{word}' removed from blacklist.")
        else:
            bot.reply_to(m, f"⚠️ Word '{word}' not found in blacklist.")
    except IndexError:
        bot.reply_to(m, "⚠️ Usage: /unblacklist <word>")

# ---------------- DELETE MESSAGES WITH BLACKLISTED WORDS ----------------
@bot.message_handler(func=lambda m: any(w in m.text.lower() for w in blacklist))
def delete_blacklisted_message(m):
    if is_admin(bot, m.chat.id, m.from_user.id):
        return
    try:
        bot.delete_message(m.chat.id, m.message_id)
    except Exception as e:
        print(f"Error deleting message: {e}")