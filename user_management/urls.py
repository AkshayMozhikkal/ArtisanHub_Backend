from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import Userdetails, AddressViewSet, MyTokenObtainPairView, UserRegister , VerifyUserView, Google_Registration, Edit_profile, Upload_image
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    
    path('token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token_refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('', Userdetails.as_view(), name='user-details' ),
    path('user_details_admin/', Userdetails_For_Admin.as_view(), name='user_details_admin' ),
    path('artisans/', Artisans.as_view(), name='artisans' ),
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
    path('citywise_filter/<str:city>/', City_wise_Search.as_view(), name='citywise_filter'),
    path('user_all_data/<int:pk>/', User_All_Data.as_view(), name='user_all_data'),
    path('locations/', Get_Locations.as_view(), name='locations'),
    path('forgotpassword/', ForgotPassword.as_view(),name = 'forgot-password'),
    path('reset_validate/<uidb64>/<token>/',reset_validate, name='reset_validate'),
    path('reset-password/<uidb64>/<token>', ResetPassword.as_view(), name='reset_password'),
    path('change_password/', ChangePasswordView.as_view(), name='change_password'),
    path('address/',AddressViewSet.as_view(), name='address' ),
    path('block_or_unblock/<int:id>/',Block_Or_Unblock.as_view(), name='block_or_unblock' ),
    
]