import jwt
from django.conf import settings
from asgiref.sync import sync_to_async
from django.contrib.auth.models import AnonymousUser

class JWTAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    async def __call__(self, scope, recieve, send):
        headers = dict(scope.get('headers', []))
        token = None
        
        for key, value in headers.items():
            if key == b'authorization':
                token = value.decode().split('Bearer ')[-1]
                break

        if token is not None:
            try:
                decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
                user = decoded_token.get('user_id')
                scope['user'] = await get_user_from_id(user)
            except jwt.ExpiredSignatureError:
                print("token expired")
                scope['user'] = AnonymousUser()
            except jwt.InvalidTokenError:
                print("invalid token")
                scope['user'] = AnonymousUser()
        else:
            print("else")
            scope['user'] = AnonymousUser()
            
        return await self.get_response(scope,recieve,send)
    
@sync_to_async
def get_user_from_id(user_id):
    from accounts.models import User
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()