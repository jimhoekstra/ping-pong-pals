from .models import Player, Game, Rating


def compute_elo(winner_elo: int, loser_elo: int, K: int = 32) -> tuple[int, int]:
    Q_winner = pow(10, winner_elo / 400)
    Q_loser = pow(10, loser_elo / 400)
    Q_total = Q_winner + Q_loser

    E_winner = Q_winner / Q_total
    E_loser = Q_loser / Q_total

    new_winner = winner_elo + round(K * (1.0 - E_winner))
    new_loser = loser_elo + round(K * (0.0 - E_loser))

    return new_winner, new_loser


class EloRating:

    def __init__(self, winner: Player, loser: Player):
        self.winner: Player = winner
        self.loser: Player = loser
        self.new_winner_rating: None | int = None
        self.new_loser_rating: None | int = None
        self.K = 32

        self.compute_new_scores()

    def compute_new_scores(self):
        self.new_winner_rating, self.new_loser_rating = compute_elo(
            self.winner.current_elo, self.loser.current_elo, self.K
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
