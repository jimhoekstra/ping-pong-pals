from django.test import TestCase, Client
from accounts.models import User, SignupKey
from scoreboard.models import Player, League


class TestCreateSignupToken(TestCase):

    def setUp(self):
        self.client = Client()

        self.user_a = User.objects.create(username='alice')
        self.user_b = User.objects.create(username='bob')
        self.user_c = User.objects.create(username='charlie')

        self.player_a = Player.objects.create(name='Alice', user=self.user_a)
        self.player_b = Player.objects.create(name='Bob', user=self.user_b)
        self.player_c = Player.objects.create(name='Charlie', user=self.user_c)

        self.league_a = League(name='League A', slug='league-a', owner=self.player_a)
        self.league_a.save()
        self.league_a.participants.add(self.player_a, self.player_b)

    def test_owner_can_see_page(self):
        self.client.force_login(self.user_a)
        response = self.client.get('/leagues/league-a')
        self.assertEqual(response.status_code, 200)

    def test_owner_can_create_key(self):
        self.client.force_login(self.user_a)
        response = self.client.post('/accounts/create-sign-up-token/league-a', follow=True)
        self.assertEqual(response.redirect_chain[0], ('/leagues/league-a', 302))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(SignupKey.objects.count(), 1)

    def test_member_can_see_page(self):
        self.client.force_login(self.user_b)
        response = self.client.get('/leagues/league-a')
        self.assertEqual(response.status_code, 200)

    def test_member_cannot_create_key(self):
        self.client.force_login(self.user_b)
        response = self.client.post('/accounts/create-sign-up-token/league-a', follow=True)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(SignupKey.objects.count(), 0)

    def test_other_cannot_see_page(self):
        self.client.force_login(self.user_c)
        response = self.client.get('/leagues/league-a')
        self.assertEqual(response.status_code, 400)
