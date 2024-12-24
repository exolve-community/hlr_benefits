import sqlite3
from flask import Flask, render_template, request
from datetime import datetime, timedelta
from user_agents import parse

app = Flask(__name__, static_url_path='/hlr_benefits/static')

# Инициализация базы данных
def init_db():
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS visits (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            visit_date TEXT,
            device_type TEXT,
            browser TEXT
        )
    """)
    conn.commit()
    conn.close()

# Добавление записи о посещении
def log_visit(user_agent):
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()
    visit_date = (datetime.now() + timedelta(hours=3)).strftime("%Y-%m-%d %H:%M:%S")
    parsed_agent = parse(user_agent)
    device_type = "Desktop" if parsed_agent.is_pc else "Mobile" if parsed_agent.is_mobile else "Other"
    browser = parsed_agent.browser.family
    cursor.execute("INSERT INTO visits (visit_date, device_type, browser) VALUES (?, ?, ?)", (visit_date, device_type, browser))
    conn.commit()
    conn.close()

# Получение всех записей о посещениях
def get_all_visits():
    conn = sqlite3.connect("visits.db")
    cursor = conn.cursor()
    cursor.execute("SELECT visit_date, device_type, browser FROM visits ORDER BY id DESC")
    visits = cursor.fetchall()
    conn.close()
    return visits

# Главная страница для маршрута /
@app.route("/")
@app.route("/hlr_benefits/")
def home():
    user_agent = request.headers.get("User-Agent")
    log_visit(user_agent)
    visits = get_all_visits()
    visit_count = len(visits)
    return render_template("index.html", visits=visits, visit_count=visit_count)

if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=7002)
