

# # import moviepy.editor as mp

# import os
# import logging
# from dotenv import load_dotenv
# from telegram import Update
# from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
# from instagrapi import Client

# # Load environment variables
# load_dotenv()

# # Set up logging
# logging.basicConfig(
#     format="%(asctime)s - %(levelname)s - %(message)s",
#     level=logging.INFO
# )

# logger = logging.getLogger(__name__)

# # Load credentials
# TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# IG_USERNAME = os.getenv("INSTAGRAM_USERNAME")
# IG_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

# # Initialize Instagram client
# cl = Client()

# # def login_instagram():
# #     try:
# #         cl.load_settings("session.json")
# #         cl.login(IG_USERNAME, IG_PASSWORD)
# #         cl.dump_settings("session.json")
# #         logger.info(" Logged in using saved session")
# #     except Exception:
# #         cl.login(IG_USERNAME, IG_PASSWORD)
# #         cl.dump_settings("session.json")
# #         logger.info(" Logged in to Instagram successfully.")
# from instagrapi.exceptions import ChallengeRequired

# def login_instagram():
#     try:
#         cl.load_settings("session.json")
#         cl.login(IG_USERNAME, IG_PASSWORD)
#         cl.dump_settings("session.json")
#         logger.info("✅ Logged in using saved session.")
#     except ChallengeRequired:
#         logger.warning("🔐 2FA Challenge required! Sending security code.")
#         cl.challenge_resolve()
#         code = input("📩 Enter the verification code sent to your phone/email: ")
#         cl.challenge_send_security_code(code)
#         cl.dump_settings("session.json")
#         logger.info("✅ 2FA login successful. Session saved.")
#     except Exception as e:
#         logger.error(f"❌ Instagram login failed: {e}")


# # Extract shortcode from Instagram URL
# def extract_shortcode(url: str) -> str:
#     parts = url.split("/")
#     for i, part in enumerate(parts):
#         if part in ["p", "reel", "tv"] and i + 1 < len(parts):
#             return parts[i + 1]
#     return None

# # Handle Instagram video link
# async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     try:
#         message = update.message.text
#         shortcode = extract_shortcode(message)

#         if not shortcode:
#             raise ValueError("Could not extract shortcode.")

#         logger.info(f"Extracted shortcode: {shortcode}")

#         # Fetch media
#         media_pk = cl.media_pk_from_code(shortcode)
#         media = cl.media_info(media_pk)

#         # Download
#         video_path = cl.video_download(media_pk)
#         logger.info(f"📥 Downloaded video: {video_path}")

#         # Upload
#         caption = media.caption_text or "Reposted via Telegram bot 🤖"
#         cl.clip_upload(video_path, caption)
#         logger.info(" Video uploaded to Instagram")

#         await context.bot.send_message(chat_id=update.effective_chat.id, text="Successfully reposted to Instagram!")
#     except Exception as e:
#         logger.error(" Error reposting video.", exc_info=True)
#         await context.bot.send_message(chat_id=update.effective_chat.id, text=" Failed to repost the video. Make sure the link is public and correct.")

# # Start command
# async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
#     await context.bot.send_message(chat_id=update.effective_chat.id, text=" Send me a public Instagram reel/post link to repost!")

# # Main
# if __name__ == "__main__":
#     logger.info(" Bot is starting...")
#     login_instagram()

#     app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
#     app.add_handler(CommandHandler("start", start))
#     app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

#     logger.info(" Bot is running...")
#     app.run_polling()




import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from instagrapi import Client
from instagrapi.exceptions import ChallengeRequired
from flask import Flask, request

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")  # e.g., https://your-app.onrender.com
PORT = int(os.environ.get("PORT", 8443))

IG_USERNAME = os.getenv("INSTAGRAM_USERNAME")
IG_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

cl = Client()

def login_instagram():
    try:
        cl.load_settings("session.json")
        cl.login(IG_USERNAME, IG_PASSWORD)
        cl.dump_settings("session.json")
        logger.info("✅ Logged in using saved session.")
    except ChallengeRequired:
        logger.warning("🔐 2FA Challenge required! Sending security code.")
        cl.challenge_resolve()
        # For deployment, you must handle 2FA outside or disable it for testing.
        code = input("📩 Enter the verification code sent to your phone/email: ")
        cl.challenge_send_security_code(code)
        cl.dump_settings("session.json")
        logger.info("✅ 2FA login successful. Session saved.")
    except Exception as e:
        logger.error(f"❌ Instagram login failed: {e}")

def extract_shortcode(url: str) -> str:
    parts = url.split("/")
    for i, part in enumerate(parts):
        if part in ["p", "reel", "tv"] and i + 1 < len(parts):
            return parts[i + 1]
    return None

async def handle_instagram_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message = update.message.text
        shortcode = extract_shortcode(message)

        if not shortcode:
            raise ValueError("Could not extract shortcode.")

        logger.info(f"Extracted shortcode: {shortcode}")

        media_pk = cl.media_pk_from_code(shortcode)
        media = cl.media_info(media_pk)

        video_path = cl.video_download(media_pk)
        logger.info(f"📥 Downloaded video: {video_path}")

        caption = media.caption_text or "Reposted via Telegram bot 🤖"
        cl.clip_upload(video_path, caption)
        logger.info("✅ Video uploaded to Instagram")

        await context.bot.send_message(chat_id=update.effective_chat.id, text="✅ Successfully reposted to Instagram!")
    except Exception as e:
        logger.error("❌ Error reposting video.", exc_info=True)
        await context.bot.send_message(chat_id=update.effective_chat.id, text="❌ Failed to repost. Make sure the link is public and correct.")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="👋 Send me a public Instagram reel/post link to repost!")

# Flask app for webhook
flask_app = Flask(__name__)

if __name__ == "__main__":
    logger.info("🚀 Bot is starting...")
    login_instagram()

    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_instagram_link))

    # Set webhook
    import asyncio
    asyncio.run(app.bot.set_webhook(url=WEBHOOK_URL + "/webhook"))
    logger.info(f"Webhook set to {WEBHOOK_URL}/webhook")

    @flask_app.route("/webhook", methods=["POST"])
    async def webhook():
        data = request.get_json(force=True)
        update = Update.de_json(data, app.bot)
        await app.update_queue.put(update)
        return {"status": "ok"}

    # Run Flask server on the specified PORT (Render requires this)
    flask_app.run(host="0.0.0.0", port=PORT)
