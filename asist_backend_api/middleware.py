from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model
from channels.db import database_sync_to_async
from channels.middleware import BaseMiddleware
from accounts.services import AuthorizationService

User = get_user_model()


@database_sync_to_async
def get_user(token_key):
    return AuthorizationService.get_user_by_token(token_key)


class TokenAuthMiddleware(BaseMiddleware):
    def __init__(self, inner):
        super().__init__(inner)

    async def __call__(self, scope, receive, send):
        try:
            headers = {i[0].decode(): i[1].decode() for i in scope["headers"]}
            query_params = scope["query_string"].decode()
            if query_params != "":
                token_key = query_params.replace("tk=", "")
            else:
                token_key = headers["authorization"].replace("Bearer ", "")
        except (ValueError, KeyError):
            token_key = None
        scope['user'] = AnonymousUser() if token_key is None else await get_user(token_key)
        return await super().__call__(scope, receive, send)
