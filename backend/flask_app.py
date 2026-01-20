"""
Flask-based backend for Data Watch Nexus
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
from datetime import datetime, timedelta
import jwt
# Use hashlib for simple password hashing instead of bcrypt for now
import hashlib
import os
import uuid
from functools import wraps

app = Flask(__name__)
# CORS configuration for development
CORS(app, origins=["http://localhost:3000", "http://localhost:8080", "http://127.0.0.1:3000", "http://127.0.0.1:8080"],
     allow_headers=["Content-Type", "Authorization"],
     allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     supports_credentials=True)

# Configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Database setup
def get_db():
    conn = sqlite3.connect("data_watch_nexus.db")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = sqlite3.connect("data_watch_nexus.db")
    cursor = conn.cursor()

    # Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id TEXT PRIMARY KEY,
            email TEXT UNIQUE NOT NULL,
            name TEXT NOT NULL,
            hashed_password TEXT NOT NULL,
            is_active BOOLEAN DEFAULT 1,
            is_admin BOOLEAN DEFAULT 0,
            preferences TEXT DEFAULT '{}',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP,
            last_login TEXT
        )
    ''')

    # Jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            company TEXT NOT NULL,
            company_logo TEXT,
            location TEXT NOT NULL,
            type TEXT NOT NULL,
            remote BOOLEAN DEFAULT 0,
            salary_min REAL,
            salary_max REAL,
            currency TEXT DEFAULT 'USD',
            description TEXT NOT NULL,
            requirements TEXT DEFAULT '[]',
            benefits TEXT DEFAULT '[]',
            tags TEXT DEFAULT '[]',
            posted_date TEXT DEFAULT CURRENT_TIMESTAMP,
            expiry_date TEXT,
            application_url TEXT,
            apply_email TEXT,
            featured BOOLEAN DEFAULT 0,
            is_active BOOLEAN DEFAULT 1,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Saved jobs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS saved_jobs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT NOT NULL,
            job_id TEXT NOT NULL,
            saved_at TEXT DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (id),
            FOREIGN KEY (job_id) REFERENCES jobs (id)
        )
    ''')

    # Records table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS records (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            description TEXT NOT NULL,
            source TEXT NOT NULL,
            category TEXT NOT NULL,
            published_date TEXT NOT NULL,
            url TEXT,
            is_active TEXT DEFAULT 'active',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            updated_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Insert sample data
    cursor.execute("SELECT COUNT(*) FROM jobs")
    if cursor.fetchone()[0] == 0:
        sample_jobs = [
            {
                "id": str(uuid.uuid4()),
                "title": "Senior Frontend Developer",
                "company": "TechCorp Inc.",
                "company_logo": "/placeholder.svg",
                "location": "San Francisco, CA",
                "type": "Full-time",
                "remote": True,
                "salary_min": 120000,
                "salary_max": 180000,
                "currency": "$",
                "description": "Join our team to build amazing user experiences with React, TypeScript, and modern web technologies.",
                "requirements": json.dumps(["React", "TypeScript", "Next.js", "5+ years experience"]),
                "benefits": json.dumps(["Health Insurance", "Remote Work", "401k Matching"]),
                "tags": json.dumps(["React", "TypeScript", "Frontend", "Remote"]),
                "posted_date": "2024-01-15T10:00:00Z",
                "application_url": "https://example.com/apply",
                "featured": True
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Product Manager",
                "company": "StartupXYZ",
                "location": "New York, NY",
                "type": "Full-time",
                "remote": False,
                "salary_min": 100000,
                "salary_max": 140000,
                "currency": "$",
                "description": "Drive product strategy and execution for our growing SaaS platform.",
                "requirements": json.dumps(["Product Management", "Agile", "3+ years experience", "Technical background"]),
                "benefits": json.dumps(["Equity Package", "Health Insurance", "Flexible PTO"]),
                "tags": json.dumps(["Product", "Strategy", "SaaS", "Agile"]),
                "posted_date": "2024-01-14T15:30:00Z",
                "featured": False
            }
        ]

        for job in sample_jobs:
            cursor.execute('''
                INSERT INTO jobs (id, title, company, company_logo, location, type, remote,
                                salary_min, salary_max, currency, description, requirements,
                                benefits, tags, posted_date, application_url, featured)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                job["id"], job["title"], job["company"], job.get("company_logo"), job["location"],
                job["type"], job["remote"], job.get("salary_min"), job.get("salary_max"), job.get("currency", "USD"),
                job["description"], job["requirements"], job["benefits"], job["tags"],
                job["posted_date"], job.get("application_url"), job["featured"]
            ))

    cursor.execute("SELECT COUNT(*) FROM records")
    if cursor.fetchone()[0] == 0:
        sample_records = [
            {
                "id": str(uuid.uuid4()),
                "title": "Machine Learning Trends 2024",
                "description": "Comprehensive analysis of machine learning trends and their impact on various industries.",
                "source": "TechInsights",
                "category": "Technology",
                "published_date": "2024-01-15T08:00:00Z",
                "url": "https://example.com/ml-trends-2024"
            },
            {
                "id": str(uuid.uuid4()),
                "title": "Remote Work Productivity Study",
                "description": "Research findings on remote work productivity and employee satisfaction.",
                "source": "Workforce Analytics",
                "category": "Business",
                "published_date": "2024-01-14T12:00:00Z",
                "url": "https://example.com/remote-work-study"
            }
        ]

        for record in sample_records:
            cursor.execute('''
                INSERT INTO records (id, title, description, source, category, published_date, url)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                record["id"], record["title"], record["description"], record["source"],
                record["category"], record["published_date"], record["url"]
            ))

    conn.commit()
    conn.close()

# Initialize database
init_db()

# Authentication middleware
def token_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"detail": "Token missing"}), 401

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.user_id = payload['sub']
        except jwt.ExpiredSignatureError:
            return jsonify({"detail": "Token expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"detail": "Invalid token"}), 401

        return f(*args, **kwargs)
    return decorated_function

# Utility functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Routes
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "version": "1.0.0"})

# Authentication routes
@app.route('/api/auth/register', methods=['POST'])
@app.route('/api/v1/auth/register', methods=['POST'])  # Keep both for compatibility
def register():
    try:
        data = request.get_json()

        if not data or not data.get('email') or not data.get('password') or not data.get('name'):
            return jsonify({"detail": "Email, password, and name are required"}), 400

        db = get_db()
        cursor = db.cursor()

        # Check if user exists
        cursor.execute("SELECT id FROM users WHERE email = ?", (data['email'],))
        if cursor.fetchone():
            db.close()
            return jsonify({"detail": "Email already registered"}), 400

        user_id = str(uuid.uuid4())
        # Use SHA256 with salt for password hashing
        salt = os.urandom(32)
        hashed_password = hashlib.pbkdf2_hmac('sha256', data['password'].encode('utf-8'), salt, 100000).hex()
        hashed_password = salt.hex() + '$' + hashed_password

        cursor.execute("""
            INSERT INTO users (id, email, name, hashed_password, preferences)
            VALUES (?, ?, ?, ?, ?)
        """, (user_id, data['email'], data['name'], hashed_password, '{}'))

        db.commit()
        db.close()

        token = create_access_token({"sub": user_id})
        return jsonify({
            "token": token,
            "user": {"id": user_id, "email": data['email'], "name": data['name']}
        })
    except Exception as e:
        return jsonify({"detail": f"Registration failed: {str(e)}"}), 500

@app.route('/api/auth/login', methods=['POST'])
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"detail": "Email and password are required"}), 400

    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (data['email'],))
    user = cursor.fetchone()

    if not user:
        db.close()
        return jsonify({"detail": "Incorrect email or password"}), 401

    # Verify password with PBKDF2
    try:
        stored_salt, stored_hash = user['hashed_password'].split('$', 1)
        salt = bytes.fromhex(stored_salt)
        computed_hash = hashlib.pbkdf2_hmac('sha256', data['password'].encode('utf-8'), salt, 100000).hex()

        if computed_hash != stored_hash:
            db.close()
            return jsonify({"detail": "Incorrect email or password"}), 401
    except:
        db.close()
        return jsonify({"detail": "Incorrect email or password"}), 401

    # Update last login
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?",
                  (datetime.utcnow().isoformat(), user['id']))
    db.commit()
    db.close()

    token = create_access_token({"sub": user['id']})
    return jsonify({
        "token": token,
        "user": {"id": user['id'], "email": user['email'], "name": user['name']}
    })

@app.route('/api/auth/me')
@app.route('/api/v1/auth/me')
@token_required
def get_current_user():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT id, email, name, preferences FROM users WHERE id = ?", (request.user_id,))
    user = cursor.fetchone()
    db.close()

    if not user:
        return jsonify({"detail": "User not found"}), 404

    user_dict = dict(user)
    user_dict['preferences'] = json.loads(user_dict['preferences'])
    return jsonify(user_dict)

# Jobs routes
@app.route('/api/jobs/')
@app.route('/api/v1/jobs/')
@token_required
def get_jobs():
    search = request.args.get('search')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))

    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM jobs WHERE is_active = 1"
    params = []

    if search:
        query += " AND (title LIKE ? OR company LIKE ? OR description LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])

    query += " ORDER BY posted_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, (page - 1) * limit])

    cursor.execute(query, params)
    jobs = cursor.fetchall()

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)").replace(" ORDER BY posted_date DESC LIMIT ? OFFSET ?", "")
    cursor.execute(count_query, params[:-2])
    total = cursor.fetchone()[0]

    # Get saved jobs for user
    cursor.execute("SELECT job_id FROM saved_jobs WHERE user_id = ?", (request.user_id,))
    saved_job_ids = {row['job_id'] for row in cursor.fetchall()}

    db.close()

    jobs_list = []
    for job in jobs:
        job_dict = dict(job)
        job_dict['requirements'] = json.loads(job_dict['requirements'])
        job_dict['benefits'] = json.loads(job_dict['benefits'])
        job_dict['tags'] = json.loads(job_dict['tags'])
        job_dict['saved'] = job_dict['id'] in saved_job_ids
        jobs_list.append(job_dict)

    return jsonify({
        "jobs": jobs_list,
        "total": total,
        "page": page,
        "total_pages": (total + limit - 1) // limit
    })

@app.route('/api/jobs/<job_id>')
@app.route('/api/v1/jobs/<job_id>')
@token_required
def get_job(job_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ? AND is_active = 1", (job_id,))
    job = cursor.fetchone()

    if not job:
        db.close()
        return jsonify({"detail": "Job not found"}), 404

    # Check if saved
    cursor.execute("SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?", (request.user_id, job_id))
    saved = cursor.fetchone() is not None

    db.close()

    job_dict = dict(job)
    job_dict['requirements'] = json.loads(job_dict['requirements'])
    job_dict['benefits'] = json.loads(job_dict['benefits'])
    job_dict['tags'] = json.loads(job_dict['tags'])
    job_dict['saved'] = saved

    return jsonify(job_dict)

@app.route('/api/jobs/save', methods=['POST'])
@app.route('/api/v1/jobs/save', methods=['POST'])
@token_required
def save_job():
    data = request.get_json()

    if not data or not data.get('job_id'):
        return jsonify({"detail": "job_id is required"}), 400

    db = get_db()
    cursor = db.cursor()

    # Check if already saved
    cursor.execute("SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?",
                  (request.user_id, data['job_id']))
    if cursor.fetchone():
        db.close()
        return jsonify({"detail": "Job already saved"}), 400

    cursor.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (?, ?)",
                  (request.user_id, data['job_id']))
    db.commit()
    db.close()

    return jsonify({"message": "Job saved successfully"})

@app.route('/api/jobs/<job_id>/save', methods=['DELETE'])
@app.route('/api/v1/jobs/<job_id>/save', methods=['DELETE'])
@token_required
def unsave_job(job_id):
    db = get_db()
    cursor = db.cursor()

    cursor.execute("DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?",
                  (request.user_id, job_id))

    if cursor.rowcount == 0:
        db.close()
        return jsonify({"detail": "Saved job not found"}), 404

    db.commit()
    db.close()

    return jsonify({"message": "Job unsaved successfully"})

@app.route('/api/jobs/saved/list')
@app.route('/api/v1/jobs/saved/list')
@token_required
def get_saved_jobs():
    db = get_db()
    cursor = db.cursor()

    cursor.execute("""
        SELECT j.* FROM jobs j
        INNER JOIN saved_jobs sj ON j.id = sj.job_id
        WHERE sj.user_id = ?
        ORDER BY sj.saved_at DESC
    """, (request.user_id,))

    jobs = cursor.fetchall()
    db.close()

    jobs_list = []
    for job in jobs:
        job_dict = dict(job)
        job_dict['requirements'] = json.loads(job_dict['requirements'])
        job_dict['benefits'] = json.loads(job_dict['benefits'])
        job_dict['tags'] = json.loads(job_dict['tags'])
        job_dict['saved'] = True
        jobs_list.append(job_dict)

    return jsonify(jobs_list)

@app.route('/api/jobs/meta/categories')
@app.route('/api/v1/jobs/meta/categories')
def get_job_categories():
    db = get_db()
    cursor = db.cursor()

    # Get all tags from jobs
    cursor.execute("SELECT tags FROM jobs WHERE is_active = 1")
    all_tags = []
    for row in cursor.fetchall():
        tags = json.loads(row['tags'])
        all_tags.extend(tags)

    db.close()

    return jsonify(list(set(all_tags)))

@app.route('/api/jobs/meta/types')
@app.route('/api/v1/jobs/meta/types')
def get_job_types():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT type FROM jobs WHERE is_active = 1")
    types = [row['type'] for row in cursor.fetchall()]
    db.close()

    return jsonify(types)

# Records routes
@app.route('/api/records/')
@app.route('/api/v1/records/')
@token_required
def get_records():
    search = request.args.get('search')
    category = request.args.get('category')
    page = int(request.args.get('page', 1))
    limit = int(request.args.get('limit', 12))

    db = get_db()
    cursor = db.cursor()

    query = "SELECT * FROM records WHERE is_active = 'active'"
    params = []

    if search:
        query += " AND (title LIKE ? OR description LIKE ? OR source LIKE ?)"
        search_param = f"%{search}%"
        params.extend([search_param, search_param, search_param])

    if category:
        query += " AND category = ?"
        params.append(category)

    query += " ORDER BY published_date DESC LIMIT ? OFFSET ?"
    params.extend([limit, (page - 1) * limit])

    cursor.execute(query, params)
    records = cursor.fetchall()

    # Get total count
    count_query = query.replace("SELECT *", "SELECT COUNT(*)").replace(" ORDER BY published_date DESC LIMIT ? OFFSET ?", "")
    cursor.execute(count_query, params[:-2])
    total = cursor.fetchone()[0]

    db.close()

    records_list = [dict(record) for record in records]

    return jsonify({
        "records": records_list,
        "total": total,
        "page": page,
        "total_pages": (total + limit - 1) // limit
    })

@app.route('/api/records/<record_id>')
@app.route('/api/v1/records/<record_id>')
@token_required
def get_record(record_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ? AND is_active = 'active'", (record_id,))
    record = cursor.fetchone()
    db.close()

    if not record:
        return jsonify({"detail": "Record not found"}), 404

    return jsonify(dict(record))

@app.route('/api/records/meta/categories')
@app.route('/api/v1/records/meta/categories')
def get_record_categories():
    db = get_db()
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT category FROM records WHERE is_active = 'active'")
    categories = [row['category'] for row in cursor.fetchall()]
    db.close()

    return jsonify(categories)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
