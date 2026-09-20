from datetime import UTC, datetime
from typing import Self

from pydantic import BaseModel
from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    hashed_password: Mapped[str] = mapped_column(String)
    is_admin: Mapped[bool] = mapped_column(Boolean)


class ProcessedUser(BaseModel):
    rank: str
    username: str
    games_played: int
    games_won: int
    elo_score: str


class Session(Base):
    __tablename__ = "sessions"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    username: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    revoked_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )


class ProcessedSession(BaseModel):
    id: str
    username: str
    created_at: datetime
    expires_at: datetime
    revoked_at: datetime | None

    @classmethod
    def from_db_session(cls, session: Session) -> Self:
        return cls(
            id=session.id,
            username=session.username,
            created_at=session.created_at,
            expires_at=session.expires_at,
            revoked_at=session.revoked_at,
        )


class SignupCode(Base):
    __tablename__ = "signup_codes"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String)
    used_by: Mapped[str | None] = mapped_column(String, ForeignKey("users.username"))
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )


class ProcessedSignupCode(BaseModel):
    code: str
    used_by: str | None
    updated_at: datetime

    @classmethod
    def from_db_signup_code(cls, signup_code: SignupCode) -> Self:
        return cls(
            code=signup_code.code,
            used_by=signup_code.used_by,
            updated_at=signup_code.updated_at,
        )


class Game(Base):
    __tablename__ = "games"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    saved_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(tz=UTC)
    )
    winner: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    loser: Mapped[str] = mapped_column(String, ForeignKey("users.username"))
    winner_points: Mapped[int] = mapped_column(Integer)
    loser_points: Mapped[int] = mapped_column(Integer)


class ProcessedGame(BaseModel):
    saved_at: str
    winner: str
    loser: str
    score: str

    @classmethod
    def from_db_game(cls, game: Game) -> Self:
        return cls(
            saved_at=game.saved_at.strftime("%b %d (%a)"),
            winner=game.winner,
            loser=game.loser,
            score=f"{game.winner_points}-{game.loser_points}",
        )
