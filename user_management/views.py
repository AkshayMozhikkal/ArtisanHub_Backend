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
from rest_framework import  generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, F
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.views import PasswordResetView, PasswordResetConfirmView
from django.views.decorators.cache import never_cache
from rest_framework.decorators import api_view
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from decouple import config





#Pagination Class
class CustomPagination(PageNumberPagination):
    page_size = 4 
    page_size_query_param = 'page_size'
    max_page_size = 100  

# Login and Token creations
class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = myTokenObtainPairSerializer
      
class Userdetails(ListAPIView):
    queryset = Uuser.objects.all().exclude(is_superuser = True).order_by('id')
    serializer_class = UuserSerializer
    lookup_field = 'id'    
  
class Userdetails_For_Admin(ListAPIView):
    queryset = Uuser.objects.all().exclude(is_superuser = True).order_by('id')
    serializer_class = UuserSerializer
    lookup_field = 'id'
    pagination_class= CustomPagination
    
class Artisans(ListAPIView):
    queryset=Uuser.objects.filter(is_artisan=True).order_by('id') 
    serializer_class = UuserSerializer 
    
class Block_Or_Unblock(UpdateAPIView):
    lookup_field='id'
    queryset = Uuser.objects.all()
    serializer_class=EditUserSerializer
    def patch(self, request, *args, **kwargs):
        user_ID = self.kwargs['id']
        block = request.data.get('is_active')       
        try:
            user= Uuser.objects.get(id=user_ID)
        except:
            return Response({"message":'User not found'}, status=status.HTTP_404_NOT_FOUND)              

        if block:    
            subject = 'ArtisanHub | Account Unblocked'
            message = f'''Hello {user.first_name} {user.last_name}, 
            Your Account has been reviewwed and activated back..! Continue to browse on ArtisanHub..'''
            from_email = 'akshay.for.career@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list)
        else:
            subject = 'ArtisanHub | Account Blocked'
            message = f'''Hello {user.first_name} {user.last_name},
            Your Account has been blocked due to some issues, Please contact admins for more details.'''
            from_email = 'akshay.for.career@gmail.com'
            recipient_list = [user.email]
            send_mail(subject, message, from_email, recipient_list) 
                      
        return super().patch(request, *args, **kwargs)      
       
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
                url = config('front_end_url') 
                redirect_url = f'{url}login' + '?message=' + message
                return HttpResponseRedirect(redirect_url)
            else:
                message = 'Activation Link expired, please register again.'
                url = config('front_end_url') 
                redirect_url = f'{url}signup' + '?message=' + message
                return HttpResponseRedirect(redirect_url)
        except Exception as e:
                message = 'Activation Link expired, please register again.'
                url = config('front_end_url') 
                redirect_url = f'{url}signup' + '?message=' + message
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
    
class City_wise_Search(ListAPIView):
    serializer_class = UuserSerializer  
    
    def get_queryset(self):
        searchkey = self.kwargs['city']
        queryset = Address.objects.filter(city__iexact=searchkey).values('user')
        user_ids = queryset.distinct()
        return Uuser.objects.filter(id__in=user_ids)


class User_All_Data(RetrieveAPIView):
    queryset = Uuser.objects.all()
    serializer_class = UserAllDataSerializer
    
    
class Get_Locations (ListAPIView):
    queryset = Address.objects.values('city').distinct()
    serializer_class = Location_Serializer 
        
    
    
class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = get_user_model()
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        user = self.request.user
        if user.is_google:
            return Response({"message": "Please try to login with google."}, status=status.HTTP_406_NOT_ACCEPTABLE)
            
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if not user.check_password(serializer.data.get("oldPass")):
                return Response({"message": "Please Enter your correct old password or try forgot password link to reset."}, status=status.HTTP_406_NOT_ACCEPTABLE)

            user.set_password(serializer.data.get("newPass"))
            user.save()
            return Response({"message": "Password successfully updated."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class ForgotPassword(APIView):
    def post(self,request):
        email = request.data.get('email')

        if Uuser.objects.filter(email=email).exists():
            user = Uuser.objects.get(email__exact=email)
            if user.is_google:
                return  Response(data={'message' : 'Please Login with google..'},status=status.HTTP_404_NOT_FOUND)
            current_site = get_current_site(request)
            domain = current_site.domain.rstrip('/')

            mail_subject = 'Click this link to change your password'
            message = render_to_string('user/forgotpassword.html',{
                'user' : user,
                'domain' : domain,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user),
                'site' : domain
            })

            to_email = email
            send_mail = EmailMessage(mail_subject,message,to=[to_email])
            send_mail.send()           

            return Response(data={'message' : 'verification email has been sent to your email address','user_id' : user.id,},status=status.HTTP_200_OK)
        else:
            return Response(data={'message' : 'No account found'},status=status.HTTP_404_NOT_FOUND)
 
        
@api_view(['GET'])
def reset_validate(request,uidb64,token): 
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Uuser._default_manager.get(pk=uid)
    except(TypeError,ValueError,Uuser.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user,token):
       url = config('front_end_url') 
       redirect_url = f'{url}resetpassword/?key={uidb64}&t={token}'
       return HttpResponseRedirect(redirect_url)
    


class ResetPassword(APIView):
    def post(self, request, uidb64, token, format=None):
        password = request.data.get('password')
        
        if uidb64 and password:  
            try:
                user_id = urlsafe_base64_decode(uidb64).decode()
                user = Uuser.objects.get(id=user_id)
                if user is not None and default_token_generator.check_token(user,token):
                    user.set_password(password)
                    user.save()
                    return Response(data={'message': 'Password has been reset successfully'}, status=status.HTTP_200_OK)
                else:
                    return Response(data={'message': 'Invalid token or user, please request for a new mail..'}, status=status.HTTP_400_BAD_REQUEST)
            except (TypeError, ValueError, OverflowError, Uuser.DoesNotExist):
                return Response(data={'message': 'Invalid token or user'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(data={'message': 'Token or password not provided'}, status=status.HTTP_400_BAD_REQUEST)    
    
      

    
    

    

    
    
 
    
    
