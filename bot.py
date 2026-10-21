import os
import logging
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

logging.basicConfig(level=logging.INFO)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()
PUBLIC_BASE_URL = os.getenv("PUBLIC_BASE_URL", "").rstrip("/")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🪪 Verify with Fayda", url=f"{PUBLIC_BASE_URL}/start")],
        [InlineKeyboardButton("ℹ️ How it works", callback_data="how_it_works")],
    ] if PUBLIC_BASE_URL else [[InlineKeyboardButton("ℹ️ How it works", callback_data="how_it_works")]]

    await update.message.reply_text(
        "Welcome to Fayda Verification Bot\\n\\n"
        "This is a development build. Fayda authentication is disabled until the "
        "official sandbox credentials and callback configuration are added.\\n\\n"
        "Never send your Fayda OTP or private identity information to this bot.",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Use /start to begin. This bot currently provides the interface only. "
        "Real authentication and identity-document retrieval must be enabled only "
        "after the official Fayda integration is configured and tested."
    )

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    if query.data == "how_it_works":
        await query.edit_message_text(
            "1. Open the secure verification page.\\n"
            "2. Continue to the official Fayda authentication service.\\n"
            "3. Complete authentication on Fayda's page.\\n"
            "4. Return to the registered callback.\\n\\n"
            "This starter build does not yet claim that a user has been verified."
        )

def main():
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN is missing. Add it in Railway Variables.")
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CallbackQueryHandler(callbacks))
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
