from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "LoomisCoin"  

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привіт! Вітаю в грі! Напиши /play, щоб почати.")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Стриб! Ти зібрав монетку! Напиши /play ще раз.")

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("play", play))
    app.run_polling()

if __name__ == "__main__":
    main()
