"""
Railway Worker - מריץ סקרייפר טבלאות פעם ביום
"""

import time
import schedule
from leagues_tables_scraper import main as run_tables_scraper
from datetime import datetime
from threading import Thread
import os

print("🏆 Railway Tables Worker התחיל!")
print(f"⏰ {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print("="*60)

def tables_scraper_job():
    """הרץ את סקרייפר הטבלאות"""
    print(f"\n📊 {datetime.now().strftime('%H:%M:%S')} - מתחיל שליפת טבלאות...")
    
    try:
        run_tables_scraper()
        print(f"✅ סיום שליפת טבלאות")
    except Exception as e:
        print(f"❌ שגיאה בסקרייפר טבלאות: {e}")

def run_api_server():
    """הרץ את Flask API"""
    from flask import Flask, jsonify
    from flask_cors import CORS
    import json
    
    app = Flask(__name__)
    CORS(app)
    
    @app.route('/')
    def home():
        return jsonify({
            'name': 'IFA Leagues Tables API',
            'version': '1.0',
            'endpoints': {
                '/api/tables': 'Get all league tables',
                '/health': 'Health check'
            }
        })
    
    @app.route('/api/tables')
    def get_tables():
        """החזר את כל טבלאות הליגה"""
        try:
            if os.path.exists('leagues_tables.json'):
                with open('leagues_tables.json', 'r', encoding='utf-8') as f:
                    tables = json.load(f)
                return jsonify(tables)
            else:
                return jsonify([])
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    @app.route('/health')
    def health():
        """בדיקת תקינות"""
        try:
            if os.path.exists('leagues_tables.json'):
                mtime = os.path.getmtime('leagues_tables.json')
                last_update = datetime.fromtimestamp(mtime).strftime('%Y-%m-%d %H:%M:%S')
                
                with open('leagues_tables.json', 'r', encoding='utf-8') as f:
                    tables = json.load(f)
                
                return jsonify({
                    'status': 'ok',
                    'last_update': last_update,
                    'total_leagues': len(tables)
                })
            else:
                return jsonify({
                    'status': 'no_data',
                    'message': 'leagues_tables.json not found'
                })
        except Exception as e:
            return jsonify({
                'status': 'error',
                'error': str(e)
            }), 500
    
    port = int(os.environ.get('PORT', 8080))
    
    # Run Flask - this will block the thread (which is fine since we're in a daemon thread)
    app.run(host='0.0.0.0', port=port, threaded=True, use_reloader=False, debug=False)

# הפעל את ה-API ב-thread נפרד קודם כל
print(f"🌐 מפעיל API Server...")
api_thread = Thread(target=run_api_server, daemon=True)
api_thread.start()

# המתן שנייה שה-API יתחיל
time.sleep(3)
print(f"✅ API Server רץ ברקע!")

# עכשיו הרץ סריקה ראשונית ברקע
print("\n🔄 מתחיל סריקה ראשונית ברקע...")
scraper_thread = Thread(target=tables_scraper_job, daemon=False)
scraper_thread.start()

# תזמן סריקה פעם ביום ב-03:00 בלילה
schedule.every().day.at("03:00").do(tables_scraper_job)

print(f"\n✅ Railway Tables Worker פעיל!")
print(f"   📊 שליפת טבלאות - פעם ביום ב-03:00")
print(f"   🔄 סריקה ראשונית רצה כעת ברקע...")
print(f"💾 תוצאות נשמרות ב-leagues_tables.json")
print(f"⌨️  הלוגים יופיעו כאן...\n")

# רוץ לנצח
while True:
    schedule.run_pending()
    time.sleep(60)  # בדוק כל דקה
