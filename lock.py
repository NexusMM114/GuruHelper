from main import bot
from database import locks

@bot.message_handler(commands=["lock"])
def lock(m):
    locks.add(m.text.split()[1])
    bot.reply_to(m,"🔒 Locked")

@bot.message_handler(commands=["unlock"])
def unlock(m):
    locks.discard(m.text.split()[1])
    bot.reply_to(m,"🔓 Unlocked")