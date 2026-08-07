from flask import Flask
import threading
import telebot
import yt_dlp
import os

TOKEN =''8889251624:AAFLjzcAYKZDhSqCrR8Mdrbt_7Yk_DPoSXk"


bot = telebot.TeleBot(TOKEN)

os.makedirs("downloads", exist_ok=True)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(
        message.chat.id,
        "🎬 YouTube ссылка ёки қўшиқ номини юборинг."
    )


@bot.message_handler(func=lambda message: True)
def download_video(message):
    text = message.text.strip()

    bot.send_message(message.chat.id, "Қидиряпман... ⏳")

    try:
        ydl_opts = {
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "format": "best[ext=mp4]/best",
            "noplaylist": True
        }

        if "youtube.com" in text or "youtu.be" in text:
            url = text
        else:
            url = "ytsearch1:" + text

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as video:
            bot.send_video(
                message.chat.id,
                video,
                timeout=600
            )

        os.remove(filename)

    except Exception as e:
        bot.send_message(
            message.chat.id,
            f"Хато: {e}"
        )


app = Flask(__name__)


@app.route("/")
def home():
    return "Bot is running"


def run_server():
    app.run(
        host="0.0.0.0",
        port=10000
    )


threading.Thread(
    target=run_server,
    daemon=True
).start()

print("Bot ишлаяпти...")

bot.infinity_polling()

