from rest_framework_simplejwt.tokens import AccessToken
from rest_framework import exceptions
from user_management.models import Uuser  

class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        authorization_header = request.META.get('HTTP_AUTHORIZATION')

        if authorization_header:
            try:
                token = authorization_header.split()[1]
                access_token = AccessToken(token)
                access_token.verify()
                
                user_id = access_token['id']

                try:                    
                    user = Uuser.objects.get(id=user_id)  
                    request.user = user
                except Uuser.DoesNotExist:                    
                    pass

            except (IndexError, exceptions.AuthenticationFailed):
                pass

        response = self.get_response(request)
        return response
