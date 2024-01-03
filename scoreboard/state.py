from django.http import HttpRequest
from scoreboard.models import League, Player


class ApplicationState:

    ACTIVE_LEAGUE_KEY: str = 'active_league'

    @classmethod
    def set_active_league(cls, request: HttpRequest, league: League):
        request.session[cls.ACTIVE_LEAGUE_KEY] = league.pk

    @classmethod
    def get_league_if_only_one(cls, request: HttpRequest) -> League | None:
        '''
        If a player is only a member of one league, return that league.
        '''
        player: Player = request.user.player  # type: ignore
        if player.leagues.count() == 1:  # type: ignore
            return player.leagues.first()  # type: ignore
        return None

    @classmethod
    def get_active_league(cls, request: HttpRequest) -> League | None:
        if cls.ACTIVE_LEAGUE_KEY in request.session:
            try:
                active_league = League.objects.get(pk=int(request.session[cls.ACTIVE_LEAGUE_KEY]))
                return active_league
            except League.DoesNotExist:
                return cls.get_league_if_only_one(request=request)
        else:
            return cls.get_league_if_only_one(request=request)

    @classmethod
    def remove_active_league(cls, request: HttpRequest):
        if cls.ACTIVE_LEAGUE_KEY in request.session:
            del request.session[cls.ACTIVE_LEAGUE_KEY]
