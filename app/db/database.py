from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite+aiosqlite:///mailbot.db"

engine = create_async_engine(DATABASE_URL)

async_session = sessionmaker(
    engine,
    expire_on_commit=False
)