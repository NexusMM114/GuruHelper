from main import bot
import random

@bot.message_handler(commands=["dice","roll"])
def roll(m):
    bot.reply_to(m, f"🎲 You rolled: {random.randint(1,6)}")

@bot.message_handler(commands=["slap","hug","shrug","runs"])
def fun_cmds(m):
    bot.reply_to(m, "😄 Fun executed!")