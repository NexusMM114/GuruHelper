def is_admin(bot, chat_id, user_id):
    admins = bot.get_chat_administrators(chat_id)
    return user_id in [a.user.id for a in admins]