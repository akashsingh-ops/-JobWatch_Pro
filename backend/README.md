# Data Watch Nexus - Backend

A production-grade Job Portal backend built with FastAPI, following Clean Architecture principles and industry best practices.

## 🏗️ Architecture Overview

### Clean Architecture Layers

```
┌─────────────────────────────────────┐
│         📱 Presentation Layer       │
│  (API Routes, Middleware, DTOs)    │
├─────────────────────────────────────┤
│         🧠 Application Layer        │
│  (Services, Use Cases, CQRS)       │
├─────────────────────────────────────┤
│         🏛️ Domain Layer             │
│  (Entities, Business Rules)        │
├─────────────────────────────────────┤
│         💾 Infrastructure Layer     │
│  (Database, External APIs, Cache)  │
└─────────────────────────────────────┘
```

### Key Technologies

- **Framework**: FastAPI (ASGI, async support)
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Cache**: Redis for sessions and caching
- **Search**: Elasticsearch for job search
- **Background Tasks**: Celery for email and notifications
- **Authentication**: JWT with refresh tokens
- **Monitoring**: Structured logging with Sentry integration

## 📁 Project Structure

```
backend/
├── app/
│   ├── api/                    # API routes and dependencies
│   │   ├── v1/
│   │   │   ├── api.py         # Main API router
│   │   │   ├── auth.py        # Authentication endpoints
│   │   │   ├── jobs.py        # Job management endpoints
│   │   │   ├── users.py       # User profile endpoints
│   │   │   └── notifications.py # Notification endpoints
│   │   └── dependencies/      # FastAPI dependencies
│   ├── core/                  # Core functionality
│   │   ├── auth.py           # JWT authentication
│   │   ├── config.py         # Settings management
│   │   ├── database.py       # Database connection
│   │   ├── logging.py        # Structured logging
│   │   ├── middleware.py     # Custom middleware
│   │   ├── redis.py          # Redis client
│   │   └── elasticsearch.py  # Elasticsearch client
│   ├── db/                   # Database migrations and seeds
│   ├── models/               # SQLAlchemy models
│   │   ├── base.py          # Base model classes
│   │   ├── user.py          # User models
│   │   ├── job.py           # Job models
│   │   └── notification.py  # Notification models
│   ├── schemas/             # Pydantic schemas
│   │   ├── user.py          # User schemas
│   │   ├── job.py           # Job schemas
│   │   └── notification.py  # Notification schemas
│   ├── services/            # Business logic services
│   │   ├── auth_service.py      # Authentication logic
│   │   ├── job_service.py       # Job management logic
│   │   ├── recommendation_service.py # AI-powered recommendations
│   │   └── notification_service.py   # Notification system
│   ├── tasks/               # Celery background tasks
│   ├── utils/               # Utility functions
│   └── workers/             # Background workers
├── tests/                  # Test suite
│   ├── unit/              # Unit tests
│   ├── integration/       # Integration tests
│   └── e2e/               # End-to-end tests
├── scripts/               # Utility scripts
├── deployments/           # Deployment configurations
├── requirements.txt       # Python dependencies
├── requirements-dev.txt   # Development dependencies
├── env_example.txt        # Environment variables template
├── main.py               # Application entry point
└── README.md             # This file
```

## 🚀 Quick Start

### 1. Environment Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt  # For development
```

### 2. Environment Configuration

```bash
# Copy environment template
cp env_example.txt .env

# Edit .env with your settings
# At minimum, set DATABASE_URL for PostgreSQL
```

### 3. Database Setup

```bash
# Install and start PostgreSQL
# Create database: data_watch_nexus

# Run database migrations (if using Alembic)
alembic upgrade head

# Or create tables directly
python -c "from app.core.database import create_tables; import asyncio; asyncio.run(create_tables())"
```

### 4. Start Services

```bash
# Start Redis (if not using Docker)
redis-server

# Start Elasticsearch (if not using Docker)
# Follow Elasticsearch installation guide

# Start Celery worker (for background tasks)
celery -A app.tasks worker --loglevel=info

# Start the application
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 5. Verify Installation

```bash
# Health check
curl http://localhost:8000/health

# API documentation
open http://localhost:8000/api/docs
```

## 🎯 Key Features

### 🔐 Advanced Authentication System

- **JWT Tokens**: Access + Refresh token pattern
- **Password Security**: PBKDF2 hashing with salt
- **Session Management**: Redis-based sessions
- **Role-based Access**: User roles and permissions

### 💼 Comprehensive Job Management

- **Job Posting**: Rich job descriptions with skills, requirements
- **Application Tracking**: Full application lifecycle management
- **Job Search**: Elasticsearch-powered search and filtering
- **Saved Jobs**: User job bookmarking system

### 🎯 AI-Powered Recommendations

- **Multi-algorithm Approach**:
  - Content-based filtering (skills, experience)
  - Collaborative filtering (similar users)
  - Behavioral analysis (user activity patterns)
- **Real-time Updates**: Recommendations update with profile changes
- **ML-Ready**: Architecture prepared for machine learning integration

### 👤 Advanced User Profiles

- **Comprehensive Profiles**: Skills, experience, education, preferences
- **Resume Management**: File upload with security validation
- **Profile Completeness**: Scoring system for better recommendations
- **Privacy Controls**: Visibility settings and data sharing preferences

### 📧 Production-Ready Email System

- **Async Processing**: Celery-based background email sending
- **Template System**: Jinja2 email templates
- **Delivery Tracking**: Email status monitoring
- **Multiple Providers**: SMTP failover support

### 🔔 Intelligent Notification System

- **Multi-channel**: In-app, email, push notifications
- **Event-driven**: Triggered by job matches, application updates
- **Personalization**: User preference-based delivery
- **Analytics**: Notification engagement tracking

## 🔧 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | PostgreSQL connection URL | Required |
| `REDIS_URL` | Redis connection URL | `redis://localhost:6379/0` |
| `SECRET_KEY` | JWT signing key | Auto-generated |
| `SMTP_SERVER` | Email SMTP server | `smtp.gmail.com` |
| `ELASTICSEARCH_HOST` | Elasticsearch URL | `http://localhost:9200` |

### Security Settings

- **Rate Limiting**: Configurable requests per window
- **CORS**: Configured allowed origins
- **Security Headers**: HSTS, CSP, XSS protection
- **Input Validation**: Pydantic-based validation
- **File Upload Security**: Type and size validation

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test categories
pytest tests/unit/
pytest tests/integration/
pytest tests/e2e/
```

## 📊 Monitoring & Observability

### Logging
- **Structured Logging**: JSON format for production
- **Multiple Levels**: DEBUG, INFO, WARNING, ERROR
- **Contextual Information**: Request IDs, user tracking

### Metrics
- **Health Endpoints**: `/health`, `/metrics`
- **Performance Monitoring**: Response times, error rates
- **Business Metrics**: User engagement, job applications

### Error Tracking
- **Sentry Integration**: Automatic error reporting
- **Exception Handling**: Centralized error management
- **Alerting**: Configurable error thresholds

## 🚀 Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up -d

# Or build manually
docker build -t data-watch-nexus .
docker run -p 8000:8000 data-watch-nexus
```

### Production Checklist

- [ ] Environment variables configured
- [ ] Database backups configured
- [ ] Redis persistence enabled
- [ ] Elasticsearch cluster configured
- [ ] SSL/TLS certificates installed
- [ ] Monitoring and alerting set up
- [ ] Load balancer configured
- [ ] CDN for static assets
- [ ] Rate limiting tuned
- [ ] Security headers verified

## 🤝 API Documentation

### Authentication Endpoints

```http
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET  /api/v1/auth/me
POST /api/v1/auth/logout
```

### Job Endpoints

```http
GET    /api/v1/jobs/          # List jobs with filtering
POST   /api/v1/jobs/          # Create job (admin)
GET    /api/v1/jobs/{id}      # Get job details
PUT    /api/v1/jobs/{id}      # Update job (admin)
DELETE /api/v1/jobs/{id}      # Delete job (admin)
POST   /api/v1/jobs/save      # Save/unsave job
GET    /api/v1/jobs/saved/list # Get saved jobs
```

### Application Endpoints

```http
POST   /api/v1/jobs/{job_id}/apply     # Apply for job
GET    /api/v1/applications/           # List user applications
GET    /api/v1/applications/{id}       # Get application details
PUT    /api/v1/applications/{id}/withdraw # Withdraw application
```

### Recommendation Endpoints

```http
GET    /api/v1/recommendations/jobs    # Get job recommendations
GET    /api/v1/recommendations/trending # Get trending jobs
POST   /api/v1/recommendations/feedback # Submit recommendation feedback
```

## 🔄 Background Tasks

### Celery Workers

```bash
# Email sending
celery -A app.tasks worker --pool=solo -Q emails

# Notifications
celery -A app.tasks worker --pool=solo -Q notifications

# Search indexing
celery -A app.tasks worker --pool=solo -Q search

# Analytics
celery -A app.tasks worker --pool=solo -Q analytics
```

### Periodic Tasks

- **Email cleanup**: Remove old email logs
- **Notification cleanup**: Archive old notifications
- **Analytics aggregation**: Daily metrics calculation
- **Search index optimization**: Weekly index maintenance

## 📈 Scaling Considerations

### Horizontal Scaling
- **Application**: Multiple FastAPI instances behind load balancer
- **Database**: Read replicas for query scaling
- **Cache**: Redis cluster for high availability
- **Search**: Elasticsearch cluster for search scaling

### Performance Optimization
- **Database Indexing**: Optimized indexes on frequently queried fields
- **Caching Strategy**: Multi-level caching (Redis + CDN)
- **API Optimization**: GraphQL for complex queries, pagination for large datasets
- **Background Processing**: Async task processing for heavy operations

## 🔒 Security Best Practices

### Authentication & Authorization
- JWT tokens with short expiration
- Refresh token rotation
- Password complexity requirements
- Account lockout after failed attempts

### Data Protection
- PII encryption at rest
- HTTPS everywhere
- Secure file storage with access controls
- GDPR compliance features

### API Security
- Rate limiting per user/IP
- Input validation and sanitization
- SQL injection prevention
- XSS protection

## 🤝 Contributing

1. **Code Quality**: Run tests and linting before submitting
2. **Documentation**: Update docs for API changes
3. **Security**: Follow security guidelines for new features
4. **Testing**: Add tests for new functionality

## 📄 License

This project is licensed under the MIT License.

---

**Built with ❤️ for the modern job seeker**

For questions or support, please open an issue or contact the development team.