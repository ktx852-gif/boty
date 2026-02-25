import requests
import time
from flask import Flask
import threading

# إعدادات التلجرام
TELEGRAM_TOKEN = "8521910876:AAEe2QZWRV4C38WAjWdWKqkCU1MTwK_G7gY"
CHAT_ID = "ضع_رقم_ID_حسابك_هنا" 

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    requests.post(url, json=payload)

def run_trading_logic():
    # رسالة ترحيبية فور التشغيل
    send_telegram_msg("🚀 **البوت متصل الآن!**\nجاري مراقبة الأسواق لإرسال الإشارات...")
    while True:
        time.sleep(3600)

if __name__ == "__main__":
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    run_trading_logic()
