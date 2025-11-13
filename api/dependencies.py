from typing import Optional

from fastapi import Depends
from pymongo.database import Database

from database import get_database, TweetRepository, UserRepository, TrendRepository


def get_db() -> Database:
    """Dependency for database connection."""
    return get_database()


def get_tweet_repository(db: Database = Depends(get_db)) -> TweetRepository:
    """Dependency for tweet repository."""
    return TweetRepository(db)


def get_user_repository(db: Database = Depends(get_db)) -> UserRepository:
    """Dependency for user repository."""
    return UserRepository(db)


def get_trend_repository(db: Database = Depends(get_db)) -> TrendRepository:
    """Dependency for trend repository."""
    return TrendRepository(db)
