
import telegram
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters, CallbackContext

API_TOKEN = "7959004347:AAFzxQMmXgCPCoO_oILg0e5bu8Mmij53hUM" 


async def start_function(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:

    await update.message.reply_text("oi matheus")

async def send_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.message.text == "Manda oi pro matheus":
        await update.message.reply_text(
            f"Oi, Matheus! Como é que você está?"
        )

app = ApplicationBuilder().token(API_TOKEN).build()
app.add_handler(CommandHandler("start", start_function))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_message))

if __name__ == '__main__':
    app.run_polling()