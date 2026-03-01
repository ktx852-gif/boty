import requests
import time
from flask import Flask
import threading

# --- إعدادات البوت ---
# تم وضع التوكن الخاص بك ورقم الـ ID الصحيح بناءً على صورك
TELEGRAM_TOKEN = "8521910876:AAEe2QZWRV4C38WAjWdWKqkCU1MTwK_G7gY"
CHAT_ID = "841804153" 

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل بنجاح!"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

def run_trading_logic():
    # رسالة ترحيبية تظهر لك في تلجرام عند نجاح الاتصال
    send_telegram_msg("🚀 **تم تشغيل البوت بنجاح!**\nالبوت متصل الآن بـ Render ويراقب السوق.")
    while True:
        # هنا سنضيف خوارزمية التداول (RSI/Moving Average) في الخطوة القادمة
        time.sleep(3600)

if __name__ == "__main__":
    # تشغيل Flask لإبقاء الخدمة حية على موقع Render
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    run_trading_logic()
