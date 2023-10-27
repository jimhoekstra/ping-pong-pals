from .models import Player


class EloRating:

    def __init__(self, winner: Player, loser: Player):
        self.winner: Player = winner
        self.loser: Player = loser
        self.new_winner_rating: None | int = None
        self.new_loser_rating: None | int = None
        self.K = 32

        self.compute_new_scores()

    def compute_new_scores(self):
        Q_winner: float = pow(10, self.winner.current_elo / 400)
        Q_loser: float = pow(10, self.loser.current_elo / 400)
        Q_winner_plus_Q_loser: float = Q_winner + Q_loser

        E_winner: float = Q_winner / Q_winner_plus_Q_loser
        E_loser: float = Q_loser / Q_winner_plus_Q_loser

        change_in_winner_rating: int = round(self.K * (1.0 - E_winner))
        change_in_loser_rating: int = round(self.K * (0.0 - E_loser))

        self.new_winner_rating = self.winner.current_elo + change_in_winner_rating
        self.new_loser_rating = self.loser.current_elo + change_in_loser_rating

    def commit_scores(self):
        if self.new_winner_rating is None or self.new_loser_rating is None:
            raise ValueError('new ratings have not yet been computed')
        
        self.winner.current_elo = self.new_winner_rating
        self.winner.save()

        self.loser.current_elo = self.new_loser_rating
        self.loser.save()

    def get_new_winner_rating(self):
        if self.new_winner_rating is None:
            raise ValueError('New ratings were not computed correctly')
        return self.new_winner_rating

    def get_new_loser_rating(self):
        if self.new_loser_rating is None:
            raise ValueError('New ratings were not computed correctly')
        return self.new_loser_rating
