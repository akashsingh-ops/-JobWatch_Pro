# Data Watch Nexus Backend

A comprehensive FastAPI backend for job and data record management platform with authentication, search, and real-time notifications.

## Features

- **Authentication & Authorization**: JWT-based authentication with user management
- **Job Management**: Create, search, filter, and save job postings
- **Record Management**: Store and search data records with categorization
- **Search Functionality**: Elasticsearch-powered full-text search
- **Activity Tracking**: User activity logging and analytics
- **Notifications**: Real-time notifications system
- **Caching**: Redis-based caching for improved performance
- **Background Tasks**: Celery for async task processing

## Tech Stack

- **Framework**: FastAPI
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Search**: Elasticsearch
- **Cache**: Redis
- **Authentication**: JWT tokens with bcrypt password hashing
- **Background Tasks**: Celery
- **API Documentation**: Auto-generated OpenAPI/Swagger

## Database Architecture

### Core Tables

#### Users (`users`)
- User authentication and profile information
- Preferences for personalization
- Admin role support

#### Jobs (`jobs`)
- Job postings with detailed information
- Salary ranges, requirements, benefits
- Featured job support
- Expiration dates

#### Records (`records`)
- Data entries with categorization
- Source tracking and publishing dates
- Searchable content

#### Saved Jobs (`saved_jobs`)
- User-job relationships
- Save/unsave functionality

#### User Activities (`user_activities`)
- Activity tracking for analytics
- View, save, apply actions

#### Notifications (`notifications`)
- User notifications
- Read/unread status
- Action URLs and expiration

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - User registration
- `POST /api/v1/auth/login` - User login
- `GET /api/v1/auth/me` - Get current user

### Jobs
- `GET /api/v1/jobs/` - List jobs with filtering
- `GET /api/v1/jobs/{job_id}` - Get job details
- `POST /api/v1/jobs/save` - Save a job
- `DELETE /api/v1/jobs/{job_id}/save` - Unsave a job
- `GET /api/v1/jobs/saved/list` - Get saved jobs

### Records
- `GET /api/v1/records/` - List records with filtering
- `GET /api/v1/records/{record_id}` - Get record details

### User Management
- `GET /api/v1/users/profile` - Get user profile
- `PUT /api/v1/users/profile` - Update profile
- `PUT /api/v1/users/preferences` - Update preferences

### Notifications
- `GET /api/v1/notifications/` - Get notifications
- `PUT /api/v1/notifications/{id}/read` - Mark as read

## Installation & Setup

### Prerequisites

- Python 3.9+
- PostgreSQL
- Elasticsearch 8.x
- Redis

### 1. Clone and Install Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Environment Configuration

Copy the environment example and configure:

```bash
cp env_example.txt .env
```

Edit `.env` with your configuration:

```env
# Database
DATABASE_URL=postgresql://username:password@localhost:5432/data_watch_nexus

# Elasticsearch
ELASTICSEARCH_HOST=http://localhost:9200

# Redis
REDIS_URL=redis://localhost:6379/0

# JWT
SECRET_KEY=your-super-secret-key-change-in-production
```

### 3. Database Setup

```bash
# Create database
createdb data_watch_nexus

# Run migrations (if using Alembic)
alembic upgrade head
```

### 4. Start Services

```bash
# Start Elasticsearch
# Start Redis
# Start PostgreSQL
```

### 5. Run the Application

```bash
# Development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Production
uvicorn main:app --host 0.0.0.0 --port 8000
```

## Database Schema

The application uses SQLAlchemy with async support. Tables are created automatically on startup.

### Key Relationships

```
User
├── 1:N SavedJob
├── 1:N UserActivity
└── 1:N Notification

Job
├── 1:N SavedJob
└── 1:N UserActivity

Record
└── 1:N UserActivity
```

## Elasticsearch Indices

### Jobs Index
- Full-text search on title, company, description, tags
- Filtering by location, type, remote, salary, category
- Faceted search support

### Records Index
- Full-text search on title, description, source
- Category-based filtering
- Date-based sorting

## Caching Strategy

- **User sessions**: 1 hour TTL
- **Search results**: 5 minutes TTL
- **Categories/Tags**: 30 minutes TTL
- **API responses**: 10 minutes TTL

## Background Tasks

Using Celery for:
- Email notifications
- Data indexing
- Analytics processing
- Cleanup tasks

## Security Features

- JWT token authentication
- Password hashing with bcrypt
- CORS protection
- Input validation with Pydantic
- SQL injection prevention
- XSS protection

## Performance Optimizations

- Database connection pooling
- Redis caching layer
- Elasticsearch for search queries
- Async/await for I/O operations
- Pagination for large datasets
- Database indexing on key fields

## Monitoring & Logging

- Structured logging with timestamps
- Health check endpoints
- Performance monitoring
- Error tracking
- API usage analytics

## API Documentation

Once running, visit:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
isort .
```

### Database Migrations

```bash
# Generate migration
alembic revision --autogenerate -m "Migration message"

# Apply migration
alembic upgrade head
```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Environment Variables for Production

```env
DEBUG=False
SECRET_KEY=<strong-random-key>
DATABASE_URL=<production-db-url>
ELASTICSEARCH_HOST=<production-es-url>
REDIS_URL=<production-redis-url>
ALLOWED_ORIGINS=["https://yourdomain.com"]
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make changes with tests
4. Ensure code formatting
5. Submit a pull request

## License

MIT License
