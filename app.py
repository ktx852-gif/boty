import requests
import time
import pandas as pd
from flask import Flask
import threading

# --- إعدادات البوت (بياناتك الصحيحة) ---
TELEGRAM_TOKEN = "8521910876:AAEe2QZWRV4C38WAjWdWKqkCU1MTwK_G7gY"
CHAT_ID = "841804153"
SYMBOL = "BTCUSDT"  # العملة التي سيراقبها البوت

app = Flask('')

@app.route('/')
def home():
    return "البوت يعمل ويحلل السوق الآن!"

def send_telegram_msg(message):
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "Markdown"}
    try:
        requests.post(url, json=payload)
    except:
        pass

def get_binance_data(symbol):
    """جلب بيانات السعر من بينانس"""
    url = f"https://api.binance.com/api/v3/klines?symbol={symbol}&interval=1h&limit=50"
    res = requests.get(url).json()
    df = pd.DataFrame(res, columns=['time', 'open', 'high', 'low', 'close', 'vol', 'close_time', 'qav', 'num_trades', 'taker_base', 'taker_quote', 'ignore'])
    return df['close'].astype(float)

def calculate_rsi(series, period=14):
    """حساب مؤشر RSI"""
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def run_trading_logic():
    send_telegram_msg("🟢 **تم تفعيل رادار التداول!**\nجاري مراقبة عملة BTCUSDT وإرسال الإشارات فور تحقق الشروط.")
    
    last_signal = None
    
    while True:
        try:
            prices = get_binance_data(SYMBOL)
            rsi = calculate_rsi(prices).iloc[-1]
            current_price = prices.iloc[-1]
            
            # منطق الإشارات
            if rsi < 30 and last_signal != 'buy':
                msg = f"🔔 **إشارة شراء (Buy)!**\n💰 السعر الحالي: ${current_price}\n📈 مؤشر RSI: {round(rsi, 2)}\n(السعر في منطقة دخول قوية)"
                send_telegram_msg(msg)
                last_signal = 'buy'
                
            elif rsi > 70 and last_signal != 'sell':
                msg = f"⚠️ **إشارة بيع (Sell)!**\n💰 السعر الحالي: ${current_price}\n📉 مؤشر RSI: {round(rsi, 2)}\n(السعر في منطقة جني أرباح)"
                send_telegram_msg(msg)
                last_signal = 'sell'
                
            # فحص كل دقيقة
            time.sleep(60)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(30)

if __name__ == "__main__":
    # تشغيل السيرفر
    threading.Thread(target=lambda: app.run(host='0.0.0.0', port=8080)).start()
    # تشغيل منطق التداول
    run_trading_logic()
