from django.shortcuts import render,redirect, HttpResponseRedirect
from rest_framework.generics import RetrieveUpdateDestroyAPIView, ListAPIView, CreateAPIView, ListCreateAPIView, RetrieveAPIView, GenericAPIView,UpdateAPIView
from rest_framework.request import Request
from .models import *
from .serializers import *
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework.response import Response
from rest_framework import status
from django.utils.encoding import force_str
from django.contrib.auth import get_user_model, authenticate
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from django.contrib.auth import get_user_model
from rest_framework import permissions
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView



#Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 15  
    page_size_query_param = 'page_size'
    max_page_size = 100  


# Login and Token creations
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer
    
  
class Userdetails(ListAPIView):
    queryset = Uuser.objects.all().exclude(is_superuser = True).order_by('id')
    serializer_class = UuserSerializer
    lookup_field = 'id'

class Artisans(ListAPIView):
    queryset=Uuser.objects.all().exclude(is_superuser = True, is_artisan=False).order_by('id') 
    serializer_class = UuserSerializer   
    
    
class UserRegister(CreateAPIView):
    queryset = Uuser.objects.all()
    serializer_class = UuserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
       
        # Create a user instance and set the password
        user = get_user_model()(
            username=serializer.validated_data['username'],
            email=serializer.validated_data['email'],
            first_name=serializer.validated_data.get('first_name', ''),
            last_name=serializer.validated_data.get('last_name', ''),
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        # Create a verification token
        token = default_token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))

        # Construct the verification URL
        verification_url = reverse('verify-user', kwargs={'uidb64': uid, 'token': token})

        # Send the verification email
        subject = 'ArtisanHub | Activate Your Account'
        message = f'Hi {user.first_name} {user.last_name}, Welocme to ArtisanHub..!!  Click the following link to activate your account: {request.build_absolute_uri(verification_url)}'
        from_email = 'akshay.for.career@gmail.com'
        recipient_list = [user.email]

        send_mail(subject, message, from_email, recipient_list)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
  
  
    
class VerifyUserView(GenericAPIView):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
            
            if default_token_generator.check_token(user, token):
                user.is_active = True
                user.save()
                message = 'Congrats! Account activated!'
                redirect_url = 'http://localhost:5173/login' + '?message=' + message
                return HttpResponseRedirect(redirect_url)
            else:
                message = 'Activation Link expired, please register again.'
                redirect_url = 'http://localhost:5173/signup' + '?message=' + message
                return HttpResponseRedirect(redirect_url)
        except Exception as e:
                message = 'Activation Link expired, please register again.'
                redirect_url = 'http://localhost:5173/signup' + '?message=' + message
                return HttpResponseRedirect(redirect_url)  



    
def create_jwt_pair_tokens(user):
    
    refresh = RefreshToken.for_user(user)
    refresh['username'] = user.email
    refresh['first_name'] = user.first_name
    refresh['last_name'] = user.last_name
    refresh['email'] = user.email
    refresh['is_active'] = user.is_active
    refresh['is_admin'] = user.is_superuser
    refresh['is_google'] = user.is_google
    refresh['id'] = user.id

   
    access_token = str(refresh.access_token) # type: ignore
    refresh_token = str(refresh)

    
    return {
        "access": access_token,
        "refresh": refresh_token,
    }



# Google Signup
class Google_Registration(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not Uuser.objects.filter(email=email,is_google=True).exists():
            serializer = GoogleAuthSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):

                user = serializer.save()
                user.is_active = True
                user.is_google = True
                user.set_password(password)
                user.save()
        user = authenticate(request, email=email, password=password)

        if user is not None:
            token = create_jwt_pair_tokens(user)
            response_data = {
               
                'token': token
            }

            return Response(data = token, status = status.HTTP_201_CREATED)
        else:
            return Response({'status': 'error', 'msg': serializer.errors})
 
 
class SingleUserdetails(RetrieveAPIView):
    queryset = Uuser.objects.all()
    serializer_class = UuserSerializer
    
          
        
class Upload_image(UpdateAPIView):
    lookup_field = 'id'
    queryset = Uuser.objects.all()
    serializer_class = Upload_imageSerializer        
        
    
class AddressViewSet(RetrieveUpdateDestroyAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer

    def get_object(self):
        user_id = self.kwargs.get('user_id')
        return self.queryset.get(user__id=user_id)
    
class User_With_Address(ListAPIView):
    queryset = Address.objects.all()
    serializer_class = UserWithAddressSerializer    
    

class Add_Address(CreateAPIView) :
    serializer_class = AddressSerializer    
    
class Edit_profile(UpdateAPIView):
    lookup_field = 'id'
    queryset = Uuser.objects.all().order_by('id')
    serializer_class = EditUserSerializer
    
class Search_People(ListAPIView):
    serializer_class = UuserSerializer

    def get_queryset(self):
        searchkey = self.kwargs['searchkey']
        queryset = Uuser.objects.all().exclude(is_superuser=True).order_by('first_name')

        if searchkey: 
            queryset = queryset.filter(
                Q(username__icontains=searchkey) |
                Q(first_name__icontains=searchkey) |
                Q(last_name__icontains=searchkey) |
                Q(art__icontains=searchkey) |
                Q(email__icontains=searchkey)
            )

        return queryset

class User_All_Data(RetrieveAPIView):
    queryset = Uuser.objects.all()
    serializer_class = UserAllDataSerializer
    
    
class Get_Locations (ListAPIView):
    queryset = Address.objects.values('city').distinct()
    serializer_class = Location_Serializer 
    
    
class PasswordResetAPI(CreateAPIView):
    serializer_class = PasswordResetSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            form = PasswordResetForm(request.data)
            if form.is_valid():
                form.save(request=request)
            return Response({'message': 'Password reset email sent.'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmAPI(PasswordResetView):
    template_name = 'password_reset_confirm.html'
        

    
    

    

    
    
 
    
    
