# app.py
from flask import Flask, render_template, request, redirect, url_for, session, g
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_super_secret_key' # セッション管理に必要。本番環境では複雑なものに！

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row # これで辞書形式で結果が取得できる
    return db

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    with app.app_context():
        db = get_db()
        cursor = db.cursor()
        # users テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL,
                role TEXT NOT NULL -- 'staff' or 'manager'
            )
        ''')
        # shift_requests テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shift_requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                request_date TEXT NOT NULL, -- YYYY-MM-DD
                request_time TEXT, -- 例: "9:00-14:00"
                comment TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        # shifts_confirmed テーブル
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS shifts_confirmed (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                shift_date TEXT NOT NULL, -- YYYY-MM-DD
                start_time TEXT, -- 例: "09:00"
                end_time TEXT,   -- 例: "14:00"
                break_time TEXT, -- 例: "0.5" (時間)
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        ''')
        db.commit()

# アプリ起動時にデータベースを初期化
with app.app_context():
    init_db()

# --- ルーティングの例（後で詳しく実装） ---
@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # ここにログイン処理を実装
        pass
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('role', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) # debug=Trueは開発用。本番ではFalse