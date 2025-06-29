from pyrogram import Client, filters
import yt_dlp
import os

api_id = 19519617
api_hash = "60eaa440ba5a22fd655b39472fefa503"

app = Client("my_userbot", api_id=api_id, api_hash=api_hash)

@app.on_message(filters.text & ~filters.me)
async def indir_ve_gonder(client, message):
    url = message.text.strip()

    # Sadece bağlantı içeren mesajları işle
    if not url.startswith("http"):
        return

    # Sadece belirli sitelerden gelen bağlantılar işlensin
    if not any(site in url for site in ["youtube.com", "youtu.be", "tiktok.com", "instagram.com", "facebook.com"]):
        return await message.reply("⛔ Bu bağlantı desteklenmiyor.")

    await message.reply("🔄 Video indiriliyor, lütfen bekleyin...")

    ydl_opts = {
        'outtmpl': 'video.%(ext)s',
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4',
        'quiet': True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        with open(filename, "rb") as f:
            await client.send_video(
                chat_id=message.chat.id,
                video=f,
                supports_streaming=True,
                caption="🎬 Video başarıyla indirildi."
            )
        os.remove(filename)

    except Exception as e:
        await message.reply(f"⚠️ Hata oluştu:\n{str(e)}")

app.run()
