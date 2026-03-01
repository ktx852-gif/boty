import requests
import time
import os
from flask import Flask
from dotenv import load_dotenv
import threading
import logging

# تكوين السجلات
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# تحميل المتغيرات من ملف .env
load_dotenv()

# --- إعدادات البوت ---
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

# التحقق من البيانات المطلوبة
if not TELEGRAM_TOKEN or not CHAT_ID:
    logger.error("❌ خطأ: TELEGRAM_TOKEN و CHAT_ID مطلوبة في متغيرات البيئة")
    exit(1)

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        response = requests.post(url, json=payload, timeout=10)
        response.raise_for_status()
        logger.info("✅ تم إرسال الرسالة بنجاح")
    except requests.RequestException as e:
        logger.error(f"❌ خطأ في إرسال الرسالة: {e}")

def run_trading_logic():
    send_telegram_msg("🚀 **تم تشغيل البوت بنجاح!**\nالبوت الآن متصل ويراقب الأسواق.")
    while True:
        try:
            # هنا ستوضع خوارزمية الإشارات لاحقاً
            time.sleep(3600)
        except Exception as e:
            logger.error(f"❌ خطأ في حلقة التداول: {e}")
            time.sleep(60)  # انتظر قبل المحاولة مجدداً

if __name__ == "__main__":
    try:
        # تشغيل السيرفر في الخلفية
        flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080), daemon=True)
        flask_thread.start()
        run_trading_logic()
    except KeyboardInterrupt:
        logger.info("🛑 تم إيقاف البوت")
    except Exception as e:
        logger.error(f"❌ خطأ غير متوقع: {e}")
