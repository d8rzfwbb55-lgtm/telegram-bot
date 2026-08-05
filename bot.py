import telebot
import yt_dlp
import os

TOKEN = "8889251624:AAFLjzcAYKZDhSqCrR8Mdrbt_7Yk_DPoSXk"

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Ссылка юборинг 🎬")

@bot.message_handler(func=lambda message: True)
def download_video(message):
    url = message.text

    bot.send_message(message.chat.id, "Юкланяпти... ⏳")

    try:
        if os.path.exists("video.mp4"):
            os.remove("video.mp4")

        ydl_opts = {
    "outtmpl": "downloads/%(title)s.%(ext)s",
    "format": "best",
   }
        

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            print("Telegram upload start")
            bot.send_video(message.chat.id, video,  timeout=600)
            print("Telegram upload done")
        os.remove(filename)

    except Exception as e:
        bot.send_message(message.chat.id, f"Хато: {e}")

print("Bot ишлаяпти...")
bot.infinity_polling()
