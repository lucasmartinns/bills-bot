import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()
TOKEN = os.getenv('TELEGRAM_TOKEN')

# comando /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Olá! Mande um áudio que eu vou transcrever')

# recebe áudio
async def receber_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.voice:
        # pega o arquivo de áudio
        file = await context.bot.get_file(update.message.voice.file_id)
        
        # cria pasta local para salvar áudios
        if not os.path.exists('audios'):
            os.makedirs('audios')

        # define o nome do arquivo
        file_path = f'audios/{update.message.from_user.id}_{update.message.message_id}.ogg'
        
        # baixa audio
        await file.download_to_drive(file_path)

        await update.message.reply_text(f'Áudio recebido!')

# inicia o bot
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.VOICE, receber_audio))

print('Bot rodando...')
app.run_polling()