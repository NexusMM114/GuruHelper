from telegram import Update, ChatPermissions
from telegram.ext import *
from config import *
import database as db
import time

app = ApplicationBuilder().token(BOT_TOKEN).build()
flood = {}

# ---------- ADMIN CHECK ----------
async def is_admin(update, context):
    admins = await context.bot.get_chat_administrators(update.effective_chat.id)
    return update.effective_user.id in [a.user.id for a in admins]

# ---------- START ----------
async def start(update: Update, context):
    await update.message.reply_text("🌹 Rose Clone Active\n/use /help")

# ---------- HELP ----------
async def help_cmd(update, context):
    await update.message.reply_text(
        "🌹 Rose Commands\n\n"
        "/ban /mute\n"
        "/warn\n"
        "/save /get\n"
        "/filter\n"
        "/userinfo"
    )

# ---------- WELCOME ----------
async def welcome(update, context):
    user = update.message.new_chat_members[0]
    await update.message.reply_text(f"👋 Welcome {user.first_name}")

# ---------- BAN ----------
async def ban(update, context):
    if not await is_admin(update, context): return
    user = update.message.reply_to_message.from_user.id
    await context.bot.ban_chat_member(update.effective_chat.id, user)
    await update.message.reply_text("🚫 User banned")

# ---------- MUTE ----------
async def mute(update, context):
    if not await is_admin(update, context): return
    user = update.message.reply_to_message.from_user.id
    await context.bot.restrict_chat_member(
        update.effective_chat.id,
        user,
        ChatPermissions(can_send_messages=False)
    )
    await update.message.reply_text("🔇 User muted")

# ---------- WARN ----------
async def warn(update, context):
    if not await is_admin(update, context): return
    user = update.message.reply_to_message.from_user.id
    chat = update.effective_chat.id

    row = db.cur.execute(
        "SELECT count FROM warns WHERE user_id=? AND chat_id=?",
        (user, chat)
    ).fetchone()

    count = row[0] + 1 if row else 1

    db.cur.execute("DELETE FROM warns WHERE user_id=? AND chat_id=?", (user, chat))
    db.cur.execute("INSERT INTO warns VALUES (?,?,?)", (user, chat, count))
    db.db.commit()

    if count >= WARN_LIMIT:
        await context.bot.ban_chat_member(chat, user)
        await update.message.reply_text("🚫 Auto-ban (warn limit)")
    else:
        await update.message.reply_text(f"⚠️ Warn {count}/{WARN_LIMIT}")

# ---------- NOTES ----------
async def save(update, context):
    if not await is_admin(update, context): return
    name = context.args[0]
    content = " ".join(context.args[1:])
    db.cur.execute(
        "INSERT INTO notes VALUES (?,?,?)",
        (update.effective_chat.id, name, content)
    )
    db.db.commit()
    await update.message.reply_text("📝 Note saved")

async def get(update, context):
    name = context.args[0]
    row = db.cur.execute(
        "SELECT content FROM notes WHERE chat_id=? AND name=?",
        (update.effective_chat.id, name)
    ).fetchone()
    if row:
        await update.message.reply_text(row[0])

# ---------- FILTER ----------
async def addfilter(update, context):
    if not await is_admin(update, context): return
    word = context.args[0].lower()
    db.cur.execute(
        "INSERT INTO filters VALUES (?,?)",
        (update.effective_chat.id, word)
    )
    db.db.commit()
    await update.message.reply_text("❌ Filter added")

async def filter_check(update, context):
    words = db.cur.execute(
        "SELECT word FROM filters WHERE chat_id=?",
        (update.effective_chat.id,)
    ).fetchall()
    for w in words:
        if w[0] in update.message.text.lower():
            await update.message.delete()
            break

# ---------- ANTI FLOOD ----------
async def antiflood(update, context):
    uid = update.effective_user.id
    flood.setdefault(uid, []).append(time.time())
    flood[uid] = [t for t in flood[uid] if time.time() - t < 10]
    if len(flood[uid]) > FLOOD_LIMIT:
        await update.message.delete()

# ---------- HANDLERS ----------
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("ban", ban))
app.add_handler(CommandHandler("mute", mute))
app.add_handler(CommandHandler("warn", warn))
app.add_handler(CommandHandler("save", save))
app.add_handler(CommandHandler("get", get))
app.add_handler(CommandHandler("filter", addfilter))

app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, welcome))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, filter_check))
app.add_handler(MessageHandler(filters.ALL, antiflood))

print("🌹 Rose Clone Running")
app.run_polling()
