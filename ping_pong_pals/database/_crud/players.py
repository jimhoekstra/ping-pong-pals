from typing import Self, Literal

from pydantic import BaseModel
from sqlalchemy import select, union_all, literal, func
from sqlalchemy.orm import Session as DBSession

from ping_pong_pals.database.models import Game, User


class PlayerDetails(BaseModel):
    username: str
    num_games_played: int
    num_games_won: int

    @classmethod
    def get_for_all_players(
        cls, db: DBSession, sort_by: Literal["num_games_played", "num_games_won"]
    ) -> list[Self]:
        games = union_all(
            select(Game.winner.label("user"), literal(1).label("won")),
            select(Game.loser.label("user"), literal(0).label("won")),
        ).subquery()

        statement = (
            select(
                User.username,
                func.count(games.c.user).label("num_games_played"),
                func.coalesce(func.sum(games.c.won), 0).label("num_games_won"),
            )
            .outerjoin(games, games.c.user == User.id)
            .group_by(User.id)
            .order_by(sort_by)
        )

        rows = db.execute(statement=statement).all()
        parsed_result = [
            cls(
                username=row.username,
                num_games_played=row.num_games_played,
                num_games_won=row.num_games_won,
            )
            for row in rows
        ]
        return parsed_result
