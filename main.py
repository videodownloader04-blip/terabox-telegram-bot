import os
import glob
import subprocess
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ **TeraBox Direct Video Uploader!**\n\nTeraBox ലിങ്ക് അയക്കൂ, വീഡിയോ ഫയലായി ടെലഗ്രാമിൽ അയച്ചു തരാം.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    keywords = ["terabox", "1024tera", "teraboxapp", "terasharefile", "neobox", "freeterabox", "mirrobox"]
    
    if any(k in url for k in keywords):
        msg = await update.message.reply_text("📥 **വീഡിയോ ഡൗൺലോഡ് ചെയ്യുന്നു... (ദയവായി കാത്തിരിക്കൂ)**")
        
        output_template = "video_%(id)s.%(ext)s"
        
        try:
            # yt-dlp ഉപയോഗിച്ച് സെർവറിലേക്ക് ഡൗൺലോഡ് ചെയ്യുന്നു
            cmd = f'yt-dlp -o "{output_template}" "{url}"'
            subprocess.run(cmd, shell=True, check=True)
            
            # ഡൗൺലോഡ് ആയ വീഡിയോ ഫയൽ കണ്ടെത്തുന്നു
            files = glob.glob("video_*")
            if files:
                video_file = files[0]
                await msg.edit_text("⬆️ **ടെലഗ്രാമിലേക്ക് അപ്‌ലോഡ് ചെയ്യുന്നു...**")
                
                # ടെലഗ്രാം ചാറ്റിലേക്ക് നേരിട്ട് അയക്കുന്നു
                with open(video_file, 'rb') as video:
                    await update.message.reply_video(video=video, caption="✅ **ഇതാ നിങ്ങളുടെ വീഡിയോ!**")
                
                # ഫയൽ സെർവറിൽ നിന്ന് ഡിലീറ്റ് ചെയ്യുന്നു (Clean up)
                os.remove(video_file)
                await msg.delete()
            else:
                await msg.edit_text("❌ വീഡിയോ ഡൗൺലോഡ് ചെയ്യാൻ സാധിച്ചില്ല. TeraBox ലിങ്ക് പ്രൈവറ്റ് ആണോ എന്ന് പരിശോധിക്കുക.")
        except Exception as e:
            await msg.edit_text("❌ ഡൗൺലോഡ് എറർ! ഫയൽ സൈസ് പെർമിറ്റഡ് ലിമിറ്റിൽ കൂടുതൽ ആവാം അല്ലെങ്കിൽ TeraBox ഡൗൺലോഡ് ബ്ലോക്ക് ചെയ്തതാവാം.")
            # ക്ലീനപ്പ്
            for f in glob.glob("video_*"):
                try: os.remove(f)
                except: pass
    else:
        await update.message.reply_text("ദയവായി ഒരു TeraBox ലിങ്ക് അയക്കുക.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
