from django.test import TestCase, Client


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
