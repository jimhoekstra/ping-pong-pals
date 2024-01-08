from functools import wraps

from django.http import HttpRequest

from scoreboard.errors import bad_request
from scoreboard.models import Player, League


def require_POST_params(POST_params: list[str]):
    '''
    Creates a decorator that validates the presence of POST parameters in the 
    request object.
    '''

    def decorator(func):

        @wraps(func)
        def wrapper(request: HttpRequest, *args, **kwargs):
            for POST_param in POST_params:
                if POST_param not in request.POST:
                    return bad_request(request=request)

            return func(request, *args, **kwargs)
        
        return wrapper
        
    return decorator


def verify_access_to_league(func):

    def wrapper(request: HttpRequest, *args, **kwargs):
        if not 'league' in kwargs:
            return bad_request(request=request)
        
        player: Player = request.user.player  # type: ignore
        try:
            league: League = League.objects.get(slug=kwargs['league'])
        except League.DoesNotExist:
            return bad_request(request=request)
        
        if not league in player.leagues.all():  # type: ignore
            return bad_request(request=request)
        
        return func(request, *args, **kwargs)
    
    return wrapper


def verify_owner_of_league(func):

    def wrapper(request: HttpRequest, *args, **kwargs):
        if not 'league' in kwargs:
            return bad_request(request=request)
        
        player: Player = request.user.player  # type: ignore
        try:
            league: League = League.objects.get(slug=kwargs['league'])
        except League.DoesNotExist:
            return bad_request(request=request)
        
        if not league.owner == player:  # type: ignore
            return bad_request(request=request)
        
        return func(request, *args, **kwargs)
    
    return wrapper
