import secrets
from datetime import UTC, datetime, timedelta

from sqlalchemy import select
from sqlalchemy.orm import Session as DBSession, aliased

from .crypto import hash_password, verify_password
from .models import Game, Session, SignupCode, User, ProcessedGame


class SignupCodeValidationError(Exception):
    pass


def unsafe_create_admin_user(db: DBSession, username: str, password: str) -> None:
    admin_user = User(
        username=username,
        hashed_password=hash_password(password=password),
        is_admin=True,
    )
    db.add(admin_user)
    db.commit()


def create_user(db: DBSession, username: str, password: str, signup_code: str) -> None:
    db_signup_code = get_signup_code(db=db, code=signup_code)
    if db_signup_code is None:
        raise SignupCodeValidationError()

    user = User(
        username=username,
        hashed_password=hash_password(password=password),
        is_admin=False,
    )
    db.add(user)
    db.commit()

    db_signup_code.used_by = user.id
    db_signup_code.updated_at = datetime.now(tz=UTC)
    db.commit()


def get_user_by_id(db: DBSession, user_id: int) -> User | None:
    user = db.query(User).filter(User.id == user_id).first()
    return user


def login_user_and_create_session(
    db: DBSession, username: str, password: str
) -> Session | None:
    user = db.query(User).filter(User.username == username).first()
    if user is None or not verify_password(
        password=password, hashed_password=user.hashed_password
    ):
        return None

    session = create_session(db=db, user_id=user.id)
    return session


def get_user_from_session(db: DBSession, session_id: str | None) -> User | None:
    if session_id is None:
        return None

    session = db.query(Session).filter(Session.id == session_id).first()

    if (
        session is None
        or session.expires_at.replace(tzinfo=UTC) < datetime.now(tz=UTC)
        or session.revoked_at is not None
    ):
        return None

    user = db.query(User).filter(User.id == session.user_id).first()
    return user


def create_session(db: DBSession, user_id: int) -> Session:
    session_id = secrets.token_urlsafe(32)
    session = Session(
        id=session_id,
        user_id=user_id,
        expires_at=datetime.now(tz=UTC) + timedelta(days=7),
    )
    db.add(session)
    db.commit()

    return session


def get_all_active_sessions(db: DBSession) -> list[Session]:
    sessions = (
        db.query(Session)
        .filter(
            Session.revoked_at == None,
            Session.expires_at > datetime.now(tz=UTC),
        )
        .all()
    )
    return sessions


def revoke_session(db: DBSession, session_id: str) -> None:
    session = db.query(Session).filter(Session.id == session_id).first()
    if session is not None:
        session.revoked_at = datetime.now(tz=UTC)
        db.commit()


def save_game(
    db: DBSession, winner: int, loser: int, winner_points: int, loser_points: int
) -> None:
    game = Game(
        winner=winner,
        loser=loser,
        winner_points=winner_points,
        loser_points=loser_points,
    )
    db.add(game)
    db.commit()


def get_recent_games(db: DBSession) -> list[ProcessedGame]:
    Winner = aliased(User)
    Loser = aliased(User)

    games_stmt = (
        select(
            Game.saved_at,
            Winner.username.label("winner_username"),
            Loser.username.label("loser_username"),
            Game.winner_points,
            Game.loser_points,
        )
        .join(Winner, Game.winner == Winner.id)
        .join(Loser, Game.loser == Loser.id)
        .order_by(Game.saved_at.desc())
    )

    games = db.execute(statement=games_stmt).all()
    processed_games = [
        ProcessedGame(
            saved_at=game.saved_at.strftime("%b %d (%a)"),
            winner=game.winner_username,
            loser=game.loser_username,
            score=f"{game.winner_points}-{game.loser_points}",
        )
        for game in games
    ]
    return processed_games


def get_all_user_ids(db: DBSession) -> list[int]:
    users = db.query(User).all()
    return [user.id for user in users]


def get_all_users(db: DBSession) -> tuple[list[int], list[str]]:
    users = db.query(User).all()
    return ([user.id for user in users], [user.username for user in users])


def get_id_for_username(db: DBSession, username: str) -> int | None:
    user = db.query(User).filter(User.username == username).first()
    if user is None:
        return None
    return user.id


def get_num_played_games(db: DBSession, user_id: int) -> int:
    played_games = (
        db.query(Game)
        .filter((Game.winner == user_id) | (Game.loser == user_id))
        .count()
    )
    return played_games


def get_num_won_games(db: DBSession, user_id: int) -> int:
    won_games = db.query(Game).filter(Game.winner == user_id).count()
    return won_games


def create_signup_code(db: DBSession) -> SignupCode:
    signup_code = SignupCode(code=secrets.token_urlsafe(16))
    db.add(signup_code)
    db.commit()
    return signup_code


def get_signup_code(db: DBSession, code: str) -> SignupCode | None:
    signup_code = db.query(SignupCode).filter(SignupCode.code == code).first()
    return signup_code


def get_all_signup_codes(db: DBSession) -> list[SignupCode]:
    signup_codes = db.query(SignupCode).order_by(SignupCode.updated_at.desc()).all()
    return signup_codes


def delete_signup_code(db: DBSession, code: str) -> bool:
    signup_code = db.query(SignupCode).filter(SignupCode.code == code).first()
    if signup_code is None or signup_code.used_by is not None:
        return False

    db.delete(signup_code)
    db.commit()
    return True
