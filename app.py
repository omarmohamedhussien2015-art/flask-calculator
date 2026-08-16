from flask import Flask, render_template, request
import sqlite3
from datetime import datetime

app = Flask(__name__)

# دالة لإنشاء قاعدة البيانات والجدول لو مش موجودين
def init_db():
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS calculations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            expression TEXT NOT NULL,
            result REAL NOT NULL,
            created_at TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# تشغيل إنشاء قاعدة البيانات عند بداية البرنامج
init_db()

@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    
    if request.method == 'POST':
        num1 = request.form.get('num1', type=float)
        num2 = request.form.get('num2', type=float)
        operation = request.form.get('operation')
        
        if num1 is not None and num2 is not None:
            if operation == 'add':
                result = num1 + num2
                expr = f"{num1} + {num2}"
            elif operation == 'multiply':
                result = num1 * num2
                expr = f"{num1} × {num2}"
            elif operation == 'power':
                result = num1 ** num2
                expr = f"{num1} ^ {num2}"

            # حفظ العملية في قاعدة البيانات SQLite
            now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('history.db')
            cursor = conn.cursor()
            cursor.execute('INSERT INTO calculations (expression, result, created_at) VALUES (?, ?, ?)',
                           (expr, result, now))
            conn.commit()
            conn.close()

    # جلب أحدث 5 عمليات من قاعدة البيانات لعرضها
    conn = sqlite3.connect('history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT expression, result, created_at FROM calculations ORDER BY id DESC LIMIT 5')
    history = cursor.fetchall()
    conn.close()

    return render_template('index.html', result=result, history=history)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)