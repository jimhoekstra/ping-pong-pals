from django.http import HttpRequest
from scoreboard.models import League


class ApplicationState:

    ACTIVE_LEAGUE_KEY: str = 'active_league'

    @classmethod
    def set_active_league(cls, request: HttpRequest, league: League):
        request.session[cls.ACTIVE_LEAGUE_KEY] = league.pk

    @classmethod
    def get_active_league(cls, request: HttpRequest) -> League | None:
        if cls.ACTIVE_LEAGUE_KEY in request.session:
            try:
                active_league = League.objects.get(pk=int(request.session[cls.ACTIVE_LEAGUE_KEY]))
                return active_league
            except League.DoesNotExist:
                return None
        else:
            return None

    @classmethod
    def remove_active_league(cls, request: HttpRequest):
        if cls.ACTIVE_LEAGUE_KEY in request.session:
            del request.session[cls.ACTIVE_LEAGUE_KEY]
