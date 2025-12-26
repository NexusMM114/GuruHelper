from main import bot
from config import SUDO_USERS

@bot.message_handler(commands=["gban"])
def gban(m):
    if m.from_user.id not in SUDO_USERS:
        return
    bot.reply_to(m, "🚫 Global ban executed (placeholder).")

@bot.message_handler(commands=["broadcast"])
def broadcast(m):
    if m.from_user.id not in SUDO_USERS:
        return
    msg = m.text.replace("/broadcast","").strip()
    # For real use, loop through all groups or users
    bot.reply_to(m, f"📢 Broadcast sent:\n{msg}")

@bot.message_handler(commands=["leave","restart"])
def owner_only(m):
    if m.from_user.id not in SUDO_USERS:
        return
    bot.reply_to(m, f"⚠️ Owner command executed: {m.text.split()[0]}")