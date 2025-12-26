from main import bot
from config import BOT_NAME

@bot.message_handler(commands=["id","info","stats","ping"])
def info(m):
    bot.reply_to(m, f"🔐 {BOT_NAME} User ID: `{m.from_user.id}`")

@bot.message_handler(commands=["about"])
def about(m):
    bot.reply_to(
        m,
        f"🔐 *{BOT_NAME}*\nSecure escrow & group management bot\nPowered by Guru Escrow"
    )