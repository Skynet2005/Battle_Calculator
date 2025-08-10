from __future__ import annotations

from datetime import datetime
from pathlib import Path
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, Integer, Text, UniqueConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.engine import make_url
from dotenv import load_dotenv
load_dotenv()
import os


class Base(DeclarativeBase):
    pass


def _db_path() -> str:
    # If DATABASE_URL is present, prefer it (e.g., Postgres on Neon)
    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url
    # Fallback to local SQLite in server dir
    root = Path(__file__).resolve().parents[1]
    data_dir = root / "server"
    db_file = (data_dir / "data.db").resolve().as_posix()
    return "sqlite:///" + db_file


_URL = _db_path()
url_obj = make_url(_URL)
driver = url_obj.get_dialect().name  # 'sqlite' | 'postgresql' | ...
_is_sqlite = driver == "sqlite"

# Build connection args per driver
connect_args: dict = {}
if _is_sqlite:
    connect_args["check_same_thread"] = False
else:
    # Optional SSL mode for Postgres; many free hosts require it (e.g., Neon)
    sslmode = os.getenv("DB_SSLMODE") or os.getenv("PGSSLMODE")
    if sslmode:
        connect_args["sslmode"] = sslmode

engine = create_engine(
    _URL,
    echo=False,
    future=True,
    connect_args=connect_args,
    pool_pre_ping=True,         # refresh dead/stale connections
    pool_recycle=300,           # recycle connections periodically
    pool_size=5,
    max_overflow=10,
)
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, expire_on_commit=False)


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    password_hash: Mapped[str] = mapped_column(String(255))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

    settings: Mapped["UserSettings"] = relationship(back_populates="user", uselist=False)


class UserSettings(Base):
    __tablename__ = "user_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, index=True)
    data: Mapped[str] = mapped_column(Text)  # JSON string
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(back_populates="settings")
    __table_args__ = (UniqueConstraint("user_id", name="uq_user_settings_user"),)

class SavedSetting(Base):
    __tablename__ = "user_saved_settings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), index=True)
    name: Mapped[str] = mapped_column(String(200), index=True)
    data: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user: Mapped[User] = relationship(backref="saved_settings")


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def get_user_by_username(db, username: str) -> Optional[User]:
    return db.query(User).filter(User.username == username).first()


def get_user_by_id(db, user_id: int) -> Optional[User]:
    return db.query(User).filter(User.id == user_id).first()


def create_user(db, username: str, password_hash: str) -> User:
    user = User(username=username, password_hash=password_hash)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def upsert_user_settings(db, user_id: int, json_text: str) -> UserSettings:
    row = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    if row is None:
        row = UserSettings(user_id=user_id, data=json_text)
        db.add(row)
    else:
        row.data = json_text
    db.commit()
    db.refresh(row)
    return row


def get_user_settings(db, user_id: int) -> Optional[str]:
    row = db.query(UserSettings).filter(UserSettings.user_id == user_id).first()
    return row.data if row else None


# Created Logic for review: Multiple named saved settings per user
def create_saved_setting(db, user_id: int, name: str, json_text: str) -> SavedSetting:
    item = SavedSetting(user_id=user_id, name=name, data=json_text)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item


def list_saved_settings(db, user_id: int) -> list[SavedSetting]:
    return (
        db.query(SavedSetting)
        .filter(SavedSetting.user_id == user_id)
        .order_by(SavedSetting.updated_at.desc())
        .all()
    )


def get_saved_setting(db, user_id: int, setting_id: int) -> Optional[SavedSetting]:
    return (
        db.query(SavedSetting)
        .filter(SavedSetting.user_id == user_id, SavedSetting.id == setting_id)
        .first()
    )


def delete_saved_setting(db, user_id: int, setting_id: int) -> bool:
    row = db.query(SavedSetting).filter(SavedSetting.user_id == user_id, SavedSetting.id == setting_id).first()
    if not row:
        return False
    db.delete(row)
    db.commit()
    return True


