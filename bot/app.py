from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes

from config import settings
from logging_config import logger

bot_token = settings.bot_token.get_secret_value()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    username = user.username or "—"
    logger.info(f"/start by {user.first_name} (id={user.id}, username={username})")

    try:
        member = await context.bot.get_chat_member(
            chat_id=settings.channel_username, user_id=user.id
        )
        status = member.status

        if status in ("member", "administrator", "creator"):
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🎯 Открыть колесо удачи!",
                            web_app=WebAppInfo(url=settings.webapp_url),
                        )
                    ]
                ]
            )

            await update.message.reply_text(
                f"Привет, {user.first_name}! 👋 Спасибо за подписку на наш канал!",
                reply_markup=keyboard,
            )
        else:
            await update.message.reply_text(
                "😕 Похоже, ты ещё не подписан на наш канал.\n"
                f"Пожалуйста, подпишись: {settings.channel_username}",
                reply_markup=None,
            )

    except Exception:
        await update.message.reply_text("⚠️ Не удалось проверить подписку.")
        logger.exception("Failed to verify subscription")


async def help(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("Используй /start, чтобы начать 🔄")


if __name__ == "__main__":
    app = Application.builder().token(bot_token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help))
    logger.info("Bot is up and running...")
    app.run_polling()
