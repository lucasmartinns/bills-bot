import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Mande um áudio que eu vou transcrever')

async def receber_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        file = await context.bot.get_file(update.message.voice.file_id)
        
        if not os.path.exists('audios'):
            os.makedirs('audios')

        file_path = f'audios/{update.message.from_user.id}_{update.message.message_id}.ogg'
        
        await file.download_to_drive(file_path)

        await update.message.reply_text(f'Áudio recebido!')

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.VOICE, receber_audio))

print('Bot rodando...')
app.run_polling()