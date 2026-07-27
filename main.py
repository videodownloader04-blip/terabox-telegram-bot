import os
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
PRIMARY_API = "https://terabox-api-ebon-xi.vercel.app/fetch"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **Railway TeraBox Downloader Active!**\n\nഏത് TeraBox ലിങ്കും അയക്കൂ, വേഗത്തിൽ ഡൗൺലോഡ് ചെയ്യാം.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    keywords = ["terabox", "1024tera", "teraboxapp", "terasharefile", "neobox", "freeterabox", "mirrobox"]
    
    if any(k in url for k in keywords):
        msg = await update.message.reply_text("🔎 **ഡൗൺലോഡ് ലിങ്ക് വിശകലനം ചെയ്യുന്നു...**")
        
        dl_link = None
        file_name = "Video.mp4"
        
        # 1. Custom Vercel API Try ചെയ്യുന്നു
        try:
            res = requests.get(f"{PRIMARY_API}?url={url}", timeout=10).json()
            if res.get("status") == "success" and res.get("download_url"):
                dl_link = res.get("download_url")
                file_name = res.get("file_name", file_name)
        except Exception:
            pass
            
        # 2. ഫെയിൽ ആയാൽ Secondary API Try ചെയ്യുന്നു
        if not dl_link:
            try:
                sec_res = requests.get(f"https://terabox-dl.qt0.workers.dev/?url={url}", timeout=10).json()
                if sec_res.get("downloadLink"):
                    dl_link = sec_res.get("downloadLink")
                    file_name = sec_res.get("fileName", file_name)
            except Exception:
                pass

        if dl_link:
            keyboard = [
                [InlineKeyboardButton("🚀 Direct Fast Download / Stream", url=dl_link)]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await msg.edit_text(
                f"✅ **ഡൗൺലോഡ് ലിങ്ക് റെഡിയാണ്!**\n\n📁 **ഫയൽ:** {file_name}\n\nതാഴെയുള്ള ബട്ടണിൽ ക്ലിക്ക് ചെയ്ത് വീഡിയോ ഡൗൺലോഡ് ചെയ്യുകയോ സ്ട്രീം ചെയ്യുകയോ ചെയ്യാം 👇",
                reply_markup=reply_markup
            )
        else:
            await msg.edit_text("❌ ലിങ്ക് പ്രോസസ്സ് ചെയ്യാൻ സാധിച്ചില്ല. TeraBox ലിങ്ക് വാലിഡ് ആണോ എന്ന് ഉറപ്പുവരുത്തുക.")
    else:
        await update.message.reply_text("ദയവായി ഒരു കൃത്യമായ TeraBox ലിങ്ക് അയക്കുക.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
