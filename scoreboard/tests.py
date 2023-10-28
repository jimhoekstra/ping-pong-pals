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

    def test_unauthenticated_games_page(self):
        '''
        Test that games page returns a redirect to the login page if not logged in.
        '''
        response = self.client.get('/games')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login?next=/games')

    def test_unauthenticated_players_page(self):
        '''
        Test that players page returns a redirect to the login page if not logged in.
        '''
        response = self.client.get('/players')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/accounts/login?next=/players')
