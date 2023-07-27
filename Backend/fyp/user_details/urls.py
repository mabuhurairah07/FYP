from django.urls import path
from .views import SignupView,LoginView,SellerLoginView,SellerSignupView,AdminLoginView,AdminSignupView,TotalUsersView


urlpatterns = [
    path('signup/', SignupView.as_view(), name='SignUp'),
    path('login/', LoginView.as_view(), name='Login'),
    path('seller_signup/', SellerSignupView.as_view(), name='seller SignUp'),
    path('seller_login/', SellerLoginView.as_view(), name='seller Login'),
    path('admin_login/', AdminLoginView.as_view(), name='Admin Login'),
    path('admin_signup/', AdminSignupView.as_view(), name='Admin Signup'),
    path('all_users/', TotalUsersView.as_view(), name='Total_users'),

]