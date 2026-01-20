"""
Simple FastAPI backend for Data Watch Nexus
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import sqlite3
import json
from datetime import datetime, timedelta
import jwt
from passlib.hash import bcrypt
import uuid
from typing import Optional, List, Dict, Any

# Simple configuration
SECRET_KEY = "your-secret-key-change-in-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

app = FastAPI(title="Data Watch Nexus API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# JWT Security
security = HTTPBearer()

# Database setup
def get_db():
    conn = sqlite3.connect("data_watch_nexus.db")
    conn.row_factory = sqlite3.Row
    try:
        yield conn
    finally:
        conn.close()

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
                job["id"], job["title"], job["company"], job["company_logo"], job["location"],
                job["type"], job["remote"], job["salary_min"], job["salary_max"], job["currency"],
                job["description"], job["requirements"], job["benefits"], job["tags"],
                job["posted_date"], job["application_url"], job["featured"]
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

# Initialize database on startup
init_db()

# Utility functions
def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        return user_id
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

# Routes
@app.get("/health")
async def health_check():
    return {"status": "healthy", "version": "1.0.0"}

# Authentication routes
@app.post("/api/v1/auth/register")
async def register(user_data: dict, db=Depends(get_db)):
    cursor = db.cursor()

    # Check if user exists
    cursor.execute("SELECT id FROM users WHERE email = ?", (user_data["email"],))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Email already registered")

    user_id = str(uuid.uuid4())
    hashed_password = bcrypt.hash(user_data["password"])

    cursor.execute("""
        INSERT INTO users (id, email, name, hashed_password, preferences)
        VALUES (?, ?, ?, ?, ?)
    """, (user_id, user_data["email"], user_data["name"], hashed_password, "{}"))

    db.commit()
    return {"token": create_access_token({"sub": user_id}), "user": {"id": user_id, "email": user_data["email"], "name": user_data["name"]}}

@app.post("/api/v1/auth/login")
async def login(login_data: dict, db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ?", (login_data["email"],))
    user = cursor.fetchone()

    if not user or not bcrypt.verify(login_data["password"], user["hashed_password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")

    # Update last login
    cursor.execute("UPDATE users SET last_login = ? WHERE id = ?", (datetime.utcnow().isoformat(), user["id"]))
    db.commit()

    return {"token": create_access_token({"sub": user["id"]}), "user": {"id": user["id"], "email": user["email"], "name": user["name"]}}

@app.get("/api/v1/auth/me")
async def get_current_user(user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT id, email, name, preferences FROM users WHERE id = ?", (user_id,))
    user = cursor.fetchone()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)

# Jobs routes
@app.get("/api/v1/jobs/")
async def get_jobs(search: str = None, page: int = 1, limit: int = 12, user_id: str = Depends(verify_token), db=Depends(get_db)):
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
    cursor.execute("SELECT job_id FROM saved_jobs WHERE user_id = ?", (user_id,))
    saved_job_ids = {row["job_id"] for row in cursor.fetchall()}

    jobs_list = []
    for job in jobs:
        job_dict = dict(job)
        job_dict["requirements"] = json.loads(job_dict["requirements"])
        job_dict["benefits"] = json.loads(job_dict["benefits"])
        job_dict["tags"] = json.loads(job_dict["tags"])
        job_dict["saved"] = job_dict["id"] in saved_job_ids
        jobs_list.append(job_dict)

    return {
        "jobs": jobs_list,
        "total": total,
        "page": page,
        "total_pages": (total + limit - 1) // limit
    }

@app.get("/api/v1/jobs/{job_id}")
async def get_job(job_id: str, user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM jobs WHERE id = ? AND is_active = 1", (job_id,))
    job = cursor.fetchone()

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    # Check if saved
    cursor.execute("SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?", (user_id, job_id))
    saved = cursor.fetchone() is not None

    job_dict = dict(job)
    job_dict["requirements"] = json.loads(job_dict["requirements"])
    job_dict["benefits"] = json.loads(job_dict["benefits"])
    job_dict["tags"] = json.loads(job_dict["tags"])
    job_dict["saved"] = saved

    return job_dict

@app.post("/api/v1/jobs/save")
async def save_job(job_data: dict, user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()

    # Check if already saved
    cursor.execute("SELECT 1 FROM saved_jobs WHERE user_id = ? AND job_id = ?", (user_id, job_data["job_id"]))
    if cursor.fetchone():
        raise HTTPException(status_code=400, detail="Job already saved")

    cursor.execute("INSERT INTO saved_jobs (user_id, job_id) VALUES (?, ?)", (user_id, job_data["job_id"]))
    db.commit()

    return {"message": "Job saved successfully"}

@app.delete("/api/v1/jobs/{job_id}/save")
async def unsave_job(job_id: str, user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("DELETE FROM saved_jobs WHERE user_id = ? AND job_id = ?", (user_id, job_id))
    if cursor.rowcount == 0:
        raise HTTPException(status_code=404, detail="Saved job not found")

    db.commit()
    return {"message": "Job unsaved successfully"}

@app.get("/api/v1/jobs/saved/list")
async def get_saved_jobs(user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()

    cursor.execute("""
        SELECT j.* FROM jobs j
        INNER JOIN saved_jobs sj ON j.id = sj.job_id
        WHERE sj.user_id = ?
        ORDER BY sj.saved_at DESC
    """, (user_id,))

    jobs = cursor.fetchall()
    jobs_list = []

    for job in jobs:
        job_dict = dict(job)
        job_dict["requirements"] = json.loads(job_dict["requirements"])
        job_dict["benefits"] = json.loads(job_dict["benefits"])
        job_dict["tags"] = json.loads(job_dict["tags"])
        job_dict["saved"] = True
        jobs_list.append(job_dict)

    return jobs_list

# Records routes
@app.get("/api/v1/records/")
async def get_records(search: str = None, category: str = None, page: int = 1, limit: int = 12, user_id: str = Depends(verify_token), db=Depends(get_db)):
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

    records_list = [dict(record) for record in records]

    return {
        "records": records_list,
        "total": total,
        "page": page,
        "total_pages": (total + limit - 1) // limit
    }

@app.get("/api/v1/records/{record_id}")
async def get_record(record_id: str, user_id: str = Depends(verify_token), db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT * FROM records WHERE id = ? AND is_active = 'active'", (record_id,))
    record = cursor.fetchone()

    if not record:
        raise HTTPException(status_code=404, detail="Record not found")

    return dict(record)

@app.get("/api/v1/records/meta/categories")
async def get_categories(db=Depends(get_db)):
    cursor = db.cursor()
    cursor.execute("SELECT DISTINCT category FROM records WHERE is_active = 'active'")
    categories = [row["category"] for row in cursor.fetchall()]
    return categories

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
