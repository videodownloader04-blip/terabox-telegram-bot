from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os
import requests

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
MY_CUSTOM_API = "https://terabox-api-ebon-xi.vercel.app/fetch"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **Railway TeraBox Downloader Active!**\n\nഏത് TeraBox ലിങ്കും അയക്കൂ, ഹൈ-സ്പീഡ് ഡൗൺലോഡ് / സ്ട്രീമിംഗ് ലിങ്ക് ജനറേറ്റ് ചെയ്യാം!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    keywords = ["terabox", "1024tera", "teraboxapp", "terasharefile", "neobox", "freeterabox"]
    
    if any(k in url for k in keywords):
        msg = await update.message.reply_text("🔎 **ഡൗൺലോഡ് ലിങ്ക് തയ്യാറാക്കുന്നു...**")
        
        try:
            res = requests.get(f"{MY_CUSTOM_API}?url={url}", timeout=15).json()
            
            if res.get("status") == "success" and res.get("download_url"):
                dl_link = res.get("download_url")
                file_name = res.get("file_name", "Video.mp4")
                
                keyboard = [
                    [InlineKeyboardButton("🚀 Direct Fast Download / Stream", url=dl_link)]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await msg.edit_text(
                    f"✅ **വീഡിയോ സ്ട്രീമിംഗ് ലിങ്ക് റെഡിയാണ്!**\n\n📁 **ഫയൽ:** {file_name}\n\nതടസ്സമില്ലാതെ പ്ലേ ചെയ്യാനും വേഗത്തിൽ ഡൗൺലോഡ് ചെയ്യാനും താഴെയുള്ള ബട്ടൺ അമർത്തൂ 👇",
                    reply_markup=reply_markup
                )
            else:
                await msg.edit_text("❌ ഡൗൺലോഡ് ലിങ്ക് കിട്ടിയില്ല. TeraBox ലിങ്ക് ശരിയാണോ എന്ന് പരിശോധിക്കുക.")
        except Exception as e:
            await msg.edit_text("❌ ചെറിയൊരു കണക്ഷൻ പിശക് സംഭവിച്ചു. അൽപ്പസമയം കഴിഞ്ഞ് വീണ്ടും ശ്രമിക്കൂ.")
    else:
        await update.message.reply_text("ദയവായി ഒരു TeraBox ലിങ്ക് അയക്കുക.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
