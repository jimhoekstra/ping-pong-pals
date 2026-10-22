from sqlalchemy.orm import Session

from ping_pong_pals.database import get_db
from ping_pong_pals.database.crud import get_recent_games, update_elo_rating_for_user
from ping_pong_pals.database._crud import PlayerDetails


def compute_elo(
    winner_elo: int,
    loser_elo: int,
    K: int = 32,
    winner_points: int | None = None,
    loser_points: int | None = None,
) -> tuple[int, int]:
    Q_winner = pow(10, winner_elo / 400)
    Q_loser = pow(10, loser_elo / 400)
    Q_total = Q_winner + Q_loser

    E_winner = Q_winner / Q_total
    E_loser = Q_loser / Q_total

    # When scores are provided, use the points ratio as the actual outcome score
    # rather than a binary 1/0. A 11-0 win gives S≈1.0; an 11-10 win gives S≈0.52.
    # The two scores always sum to 1, so ratings remain zero-sum.
    # if winner_points is not None and loser_points is not None:
    #     total_points = winner_points + loser_points
    #     S_winner = winner_points / total_points
    #     S_loser = loser_points / total_points
    # else:
    S_winner = 1.0
    S_loser = 0.0

    new_winner = winner_elo + round(K * (S_winner - E_winner))
    new_loser = loser_elo + round(K * (S_loser - E_loser))

    return new_winner, new_loser


def recompute_all_scores(db: Session):
    recent_games = get_recent_games(db=db)
    player_details = PlayerDetails.get_for_all_players(db=db, sort_by="num_games_played")

    all_usernames = [player.username for player in player_details]
    username_to_score: dict[str, int] = {
        username: 1000 for username in all_usernames
    }

    oldest_to_newest_game = recent_games[::-1]
    for game in oldest_to_newest_game:
        score = game.score
        winner_score = int(score.split("-")[0])
        loser_score = int(score.split("-")[1])

        new_winner, new_loser = compute_elo(
            winner_elo=username_to_score[game.winner],
            loser_elo=username_to_score[game.loser],
            winner_points=winner_score,
            loser_points=loser_score
        )

        username_to_score[game.winner] = new_winner
        username_to_score[game.loser] = new_loser

    for username, elo_rating in username_to_score.items():
        update_elo_rating_for_user(db=db, username=username, elo_rating=elo_rating)
