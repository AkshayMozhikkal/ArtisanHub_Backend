from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Userdetails, AddressViewSet, MyTokenObtainPairView, UserRegister , VerifyUserView, Google_Registration, Edit_profile, Upload_image
from .views import *

urlpatterns = [
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', Userdetails.as_view(), name='user-details' ),
    path('details/<int:pk>/', SingleUserdetails.as_view(), name='single_user_details' ),
    path('register/',UserRegister.as_view(), name='register' ),
    path('verify/<str:uidb64>/<str:token>/', VerifyUserView.as_view(), name='verify-user'),
    path('googleRegistration/', Google_Registration.as_view(), name='googleRegistration'),
    path('edit_profile/<int:id>/', Edit_profile.as_view(), name='edit_profile'),
    path('upload_image/<int:id>/', Upload_image.as_view(), name='upload_image'),
    path('address/<int:user_id>/', AddressViewSet.as_view(), name='address'),
    path('address/add/', Add_Address.as_view(), name='add_address'),
    path('user_with_address/', User_With_Address.as_view(), name='user_with_address'),
    path('search_people/<str:searchkey>/', Search_People.as_view(), name='search_people'),
    path('user_all_data/<int:pk>/', User_All_Data.as_view(), name='user_all_data'),
    path('locations/', Get_Locations.as_view(), name='locations'),
    path('password_reset/', PasswordResetAPI.as_view(), name='password_reset'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmAPI.as_view(), name='password_reset_confirm'),
    path('password_reset/', include('django.contrib.auth.urls')),
    path('address/',AddressViewSet.as_view(), name='address' ),
    
]