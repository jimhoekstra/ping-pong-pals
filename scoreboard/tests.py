from django.test import TestCase, Client
from .elo import compute_elo


class TestComputeElo(TestCase):

    def test_equal_ratings_winner_gains_16(self):
        new_winner, _ = compute_elo(1000, 1000)
        self.assertEqual(new_winner, 1016)

    def test_equal_ratings_loser_loses_16(self):
        _, new_loser = compute_elo(1000, 1000)
        self.assertEqual(new_loser, 984)

    def test_equal_ratings_are_symmetric(self):
        new_winner, new_loser = compute_elo(1000, 1000)
        self.assertEqual(new_winner - 1000, 1000 - new_loser)

    def test_favourite_gains_fewer_points_than_underdog_on_win(self):
        # Favourite wins: small gain
        favourite_gain, _ = compute_elo(1500, 1000)
        favourite_gain -= 1500
        # Underdog wins: big gain
        underdog_gain, _ = compute_elo(1000, 1500)
        underdog_gain -= 1000
        self.assertLess(favourite_gain, underdog_gain)

    def test_favourite_loses_more_points_than_underdog_on_loss(self):
        # Favourite loses: big penalty
        _, favourite_new = compute_elo(1000, 1500)
        favourite_loss = 1500 - favourite_new
        # Underdog loses: small penalty
        _, underdog_new = compute_elo(1500, 1000)
        underdog_loss = 1000 - underdog_new
        self.assertGreater(favourite_loss, underdog_loss)

    def test_custom_k_factor(self):
        new_winner, new_loser = compute_elo(1000, 1000, K=16)
        self.assertEqual(new_winner, 1008)
        self.assertEqual(new_loser, 992)

    def test_returns_integers(self):
        new_winner, new_loser = compute_elo(1200, 1100)
        self.assertIsInstance(new_winner, int)
        self.assertIsInstance(new_loser, int)


class TestPages(TestCase):

    def setUp(self):
        self.client = Client()

    def test_home_page(self):
        '''
        Test that home page return a 200 status without being logged in.
        '''
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_leagues_page(self):
        '''
        Test that leagues page returns a redirect to the login page if not logged in.
        '''
        response = self.client.get('/leagues', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/accounts/login?next=/leagues', 302))
        self.assertEqual(response.status_code, 200)
    
    def test_unauthenticated_games_page(self):
        '''
        Test that games page returns a redirect to the login page if not logged in.
        '''
        response = self.client.get('/games', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/accounts/login?next=/games', 302))
        self.assertEqual(response.status_code, 200)

    def test_unauthenticated_players_page(self):
        '''
        Test that players page returns a redirect to the login page if not logged in.
        '''
        response = self.client.get('/players', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/accounts/login?next=/players', 302))
        self.assertEqual(response.status_code, 200)
