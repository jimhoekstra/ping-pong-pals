from .models import Player, Game, Rating


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
    if winner_points is not None and loser_points is not None:
        total_points = winner_points + loser_points
        S_winner = winner_points / total_points
        S_loser = loser_points / total_points
    else:
        S_winner = 1.0
        S_loser = 0.0

    new_winner = winner_elo + round(K * (S_winner - E_winner))
    new_loser = loser_elo + round(K * (S_loser - E_loser))

    return new_winner, new_loser


class EloRating:

    def __init__(
        self,
        winner: Player,
        loser: Player,
        winner_points: int | None = None,
        loser_points: int | None = None,
    ):
        self.winner: Player = winner
        self.loser: Player = loser
        self.winner_points: int | None = winner_points
        self.loser_points: int | None = loser_points
        self.new_winner_rating: None | int = None
        self.new_loser_rating: None | int = None
        self.K = 32

        self.compute_new_scores()

    def compute_new_scores(self):
        self.new_winner_rating, self.new_loser_rating = compute_elo(
            self.winner.current_elo,
            self.loser.current_elo,
            self.K,
            self.winner_points,
            self.loser_points,
        )

    def commit_scores(self, game: Game):
        if self.new_winner_rating is None or self.new_loser_rating is None:
            raise ValueError('new ratings have not yet been computed')
        
        self.winner.current_elo = self.new_winner_rating
        self.winner.save()

        self.loser.current_elo = self.new_loser_rating
        self.loser.save()
        
        new_winner_player_score = Rating(
            player=self.winner,
            rating=self.new_winner_rating,
            result_of_game=game
        )
        new_winner_player_score.save()

        new_loser_player_score = Rating(
            player=self.loser,
            rating=self.new_loser_rating,
            result_of_game=game
        )
        new_loser_player_score.save()

    def get_new_winner_rating(self):
        if self.new_winner_rating is None:
            raise ValueError('New ratings were not computed correctly')
        return self.new_winner_rating

    def get_new_loser_rating(self):
        if self.new_loser_rating is None:
            raise ValueError('New ratings were not computed correctly')
        return self.new_loser_rating
