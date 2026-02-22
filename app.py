from flask import Flask, render_template, request, jsonify
import sqlite3
import datetime

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    conn.execute('''
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category TEXT NOT NULL,
            description TEXT NOT NULL,
            location TEXT NOT NULL,
            latitude REAL,
            longitude REAL,
            timestamp TEXT NOT NULL,
            status TEXT DEFAULT 'open'
        )
    ''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/reports', methods=['POST'])
def submit_report():
    data = request.get_json()
    conn = get_db()
    conn.execute('''
        INSERT INTO reports (category, description, location, latitude, longitude, timestamp)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        data['category'],
        data['description'],
        data['location'],
        data['latitude'],
        data['longitude'],
        datetime.datetime.now().isoformat()
    ))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Report submitted successfully'}), 201

@app.route('/api/reports', methods=['GET'])
def get_reports():
    conn = get_db()
    reports = conn.execute('SELECT * FROM reports ORDER BY timestamp DESC').fetchall()
    conn.close()
    return jsonify([dict(r) for r in reports])

@app.route('/api/reports/<int:report_id>/status', methods=['PATCH'])
def update_status(report_id):
    data = request.get_json()
    conn = get_db()
    conn.execute(
        'UPDATE reports SET status = ? WHERE id = ?',
        (data['status'], report_id)
    )
    conn.commit()
    conn.close()
    return jsonify({'message': 'Status updated'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    conn = get_db()
    total = conn.execute('SELECT COUNT(*) FROM reports').fetchone()[0]
    resolved = conn.execute('SELECT COUNT(*) FROM reports WHERE status = "resolved"').fetchone()[0]
    top_category = conn.execute(
        'SELECT category, COUNT(*) as count FROM reports GROUP BY category ORDER BY count DESC LIMIT 1'
    ).fetchone()
    conn.close()
    return jsonify({
        'total': total,
        'resolved': resolved,
        'resolution_rate': round((resolved / total * 100) if total > 0 else 0, 1),
        'top_category': top_category['category'] if top_category else 'None'
    })

if __name__ == '__main__':
    init_db()
    app.run(debug=True)