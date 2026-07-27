import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

# Multi-API Engine for 100% Success Rate
API_LIST = [
    "https://terabox-api-ebon-xi.vercel.app/fetch?url=",
    "https://terabox-dl.qt0.workers.dev/?url=",
    "https://terabox.hnn.workers.dev/?url=",
    "https://api.terabox.app/api?url="
]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **TeraBox Downloader Active!**\n\nഏത് TeraBox / Terasharefile / 1024tera ലിങ്കും അയക്കൂ, ഹൈ-സ്പീഡ് ലിങ്ക് എടുത്ത് തരാം.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    keywords = ["terabox", "1024tera", "teraboxapp", "terasharefile", "neobox", "freeterabox", "mirrobox", "momoleech"]
    
    if any(k in url for k in keywords):
        msg = await update.message.reply_text("🔎 **ഡൗൺലോഡ് ലിങ്ക് തിരയുന്നു...**")
        
        dl_link = None
        file_name = "TeraBox_Video.mp4"
        
        # ഓരോ API ആയി മാറി മാറി ട്രൈ ചെയ്യുന്നു
        for api_url in API_LIST:
            try:
                res = requests.get(f"{api_url}{url}", timeout=8).json()
                
                # Vercel custom & worker check
                if res.get("status") == "success" and res.get("download_url"):
                    dl_link = res.get("download_url")
                    file_name = res.get("file_name", file_name)
                    break
                elif res.get("downloadLink"):
                    dl_link = res.get("downloadLink")
                    file_name = res.get("fileName", file_name)
                    break
                elif res.get("url"):
                    dl_link = res.get("url")
                    break
            except Exception:
                continue

        if dl_link:
            keyboard = [
                [InlineKeyboardButton("🚀 Direct Fast Download / Stream", url=dl_link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await msg.edit_text(
                f"✅ **വീഡിയോ ലിങ്ക് തയ്യാറാണ്!**\n\n📁 **ഫയൽ:** {file_name}\n\nതാഴെയുള്ള ബട്ടൺ ക്ലിക്ക് ചെയ്ത് പ്ലേ ചെയ്യുകയോ വേഗത്തിൽ ഡൗൺലോഡ് ചെയ്യുകയോ ചെയ്യാം 👇",
                reply_markup=reply_markup
            )
        else:
            await msg.edit_text("❌ ലിങ്ക് പ്രോസസ്സ് ചെയ്യാൻ സാധിച്ചില്ല. ഈ ലിങ്ക് Private ആയതോ അല്ലെങ്കിൽ സപ്പോർട്ട് ചെയ്യാത്തതോ ആകാം. മറ്റൊരു ലിങ്ക് അയച്ച് നോക്കൂ.")
    else:
        await update.message.reply_text("ദയവായി ഒരു കൃത്യമായ TeraBox ലിങ്ക് അയക്കുക.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
