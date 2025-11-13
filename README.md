# Twitter Scraping Bot

A comprehensive, production-ready Twitter scraping bot that collects tweets, user data, and trending topics with support for both API-based and non-API scraping methods.

## Features

- **Multi-Source Scraping**: Twitter API v2 + SNScrape fallback
- **Flexible Search**: By keyword, hashtag, date range, and geolocation
- **Data Extraction**: Tweets, user profiles, engagement metrics, trending topics
- **Storage**: MongoDB database integration
- **Scheduling**: Automated scraping with Celery + Redis
- **REST API**: FastAPI endpoints for data access and export
- **Sentiment Analysis**: Optional TextBlob integration
- **Containerization**: Docker and Docker Compose support
- **Error Handling**: Retry logic, rate limiting, comprehensive logging

## Project Structure

```
twitter-bot/
├── api/                    # FastAPI routes
│   ├── __init__.py
│   ├── main.py            # FastAPI application
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── tweets.py
│   │   ├── users.py
│   │   ├── trends.py
│   │   └── export.py
│   └── dependencies.py
├── scraper/               # Scraping logic
│   ├── __init__.py
│   ├── twitter_api.py    # Twitter API v2 client
│   ├── snscrape_client.py # SNScrape implementation
│   └── base.py           # Abstract base scraper
├── database/             # MongoDB models
│   ├── __init__.py
│   ├── connection.py
│   └── models.py
├── tasks/                # Celery tasks
│   ├── __init__.py
│   ├── celery_app.py
│   └── scraping_tasks.py
├── config/               # Configuration
│   ├── __init__.py
│   ├── settings.py
│   └── config.yaml
├── utils/                # Utilities
│   ├── __init__.py
│   ├── logger.py
│   ├── sentiment.py
│   └── helpers.py
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_api.py
│   └── test_scraper.py
├── .env.example          # Environment variables template
├── .gitignore
├── requirements.txt      # Python dependencies
├── Dockerfile
├── docker-compose.yml
└── main.py              # Application entry point
```

## Prerequisites

- Python 3.9+
- Docker & Docker Compose
- MongoDB
- Redis
- Twitter API credentials (optional, for API-based scraping)

## Installation

### 1. Clone and Setup

```bash
cd "c:\Users\alooh\Desktop\Twitter Bot"
```

### 2. Configure Environment

Copy the example environment file and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your settings:
- Twitter API credentials (if using API)
- MongoDB connection string
- Redis connection string

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Scraping Parameters

Edit `config/config.yaml` to set:
- Keywords to track
- Scraping intervals
- API preferences
- Rate limits

## Running with Docker

### Start All Services

```bash
docker-compose up -d
```

This starts:
- FastAPI server (port 8000)
- MongoDB (port 27017)
- Redis (port 6379)
- Celery worker
- Celery beat (scheduler)

### View Logs

```bash
docker-compose logs -f
```

### Stop Services

```bash
docker-compose down
```

## Running Locally

### 1. Start MongoDB and Redis

Ensure MongoDB and Redis are running locally or via Docker:

```bash
docker run -d -p 27017:27017 --name mongodb mongo:latest
docker run -d -p 6379:6379 --name redis redis:latest
```

### 2. Start FastAPI Server

```bash
python main.py
```

Or with uvicorn:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Start Celery Worker

In a new terminal:

```bash
celery -A tasks.celery_app worker --loglevel=info
```

### 4. Start Celery Beat (Scheduler)

In another terminal:

```bash
celery -A tasks.celery_app beat --loglevel=info
```

## API Endpoints

### Get Tweets

```bash
GET /api/v1/tweets?keyword=AI&limit=100&start_date=2025-01-01
```

Parameters:
- `keyword` (required): Search term or hashtag
- `limit` (optional): Number of tweets (default: 100)
- `start_date` (optional): Start date (YYYY-MM-DD)
- `end_date` (optional): End date (YYYY-MM-DD)
- `lang` (optional): Language code (e.g., 'en')

### Get User Data

```bash
GET /api/v1/users/{username}
```

### Get Trending Topics

```bash
GET /api/v1/trends?location=global
```

Parameters:
- `location` (optional): Location name or WOEID (default: 'global')

### Export Data

```bash
GET /api/v1/export?format=csv&keyword=AI&limit=1000
```

Parameters:
- `format` (required): 'csv' or 'json'
- `keyword` (optional): Filter by keyword
- `limit` (optional): Number of records

### Trigger Manual Scrape

```bash
POST /api/v1/scrape
Content-Type: application/json

{
  "keyword": "AI startups",
  "limit": 500,
  "start_date": "2025-01-01"
}
```

## API Documentation

Once running, visit:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Configuration

### config.yaml

```yaml
scraping:
  keywords:
    - "AI"
    - "machine learning"
    - "#python"
  
  schedule:
    interval_minutes: 60
  
  limits:
    tweets_per_run: 1000
    retry_attempts: 3
    rate_limit_delay: 15

api:
  use_twitter_api: true
  fallback_to_snscrape: true

database:
  cleanup_days: 30
```

## Database Schema

### Tweets Collection

```json
{
  "_id": "ObjectId",
  "tweet_id": "string",
  "text": "string",
  "created_at": "datetime",
  "lang": "string",
  "user": {
    "username": "string",
    "name": "string",
    "followers": "number",
    "verified": "boolean"
  },
  "metrics": {
    "likes": "number",
    "retweets": "number",
    "replies": "number"
  },
  "sentiment": {
    "polarity": "number",
    "subjectivity": "number",
    "label": "string"
  },
  "scraped_at": "datetime"
}
```

## Monitoring

### Check Celery Tasks

```bash
celery -A tasks.celery_app inspect active
```

### View MongoDB Data

```bash
docker exec -it mongodb mongosh
use twitter_db
db.tweets.find().limit(5)
```

## Development

### Running Tests

```bash
pytest tests/ -v
```

### Code Formatting

```bash
black .
isort .
```

### Type Checking

```bash
mypy .
```

## Troubleshooting

### Rate Limiting

If you encounter rate limits:
- Increase `rate_limit_delay` in config.yaml
- Enable `fallback_to_snscrape` for non-API scraping
- Reduce scraping frequency

### MongoDB Connection Issues

Check connection string in .env:
```
MONGODB_URI=mongodb://localhost:27017/twitter_db
```

### Celery Not Processing Tasks

Ensure Redis is running:
```bash
docker ps | grep redis
```

## Security Notes

- Never commit `.env` file with real credentials
- Use environment variables for sensitive data
- Implement rate limiting in production
- Monitor API usage to avoid Twitter API limits
- Comply with Twitter's Terms of Service

## Advanced Features

### Sentiment Analysis

Enable in config.yaml:
```yaml
features:
  sentiment_analysis: true
```

### Custom Alerts

Configure Telegram/Slack webhooks in .env for trending alerts.

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## Support

For issues and questions:
- Open an issue on GitHub
- Check documentation at /docs

## Roadmap

- [ ] Dashboard UI (Next.js/React)
- [ ] Real-time streaming support
- [ ] Advanced analytics module
- [ ] Multi-platform support (Facebook, Instagram)
- [ ] Machine learning classification
- [ ] GraphQL API

---

**Note**: This bot is for educational purposes. Ensure compliance with Twitter's Terms of Service and API usage policies.
