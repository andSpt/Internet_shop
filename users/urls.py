from django.urls import path
from django.contrib.auth.decorators import login_required

from users.views import login, UserRegistrationView, UserProfileView, logout


app_name = 'users'

urlpatterns = [
    path('login/', login, name='login'),
    path('registration/', login_required(UserRegistrationView.as_view()), name='registration'),
    path('profile/<int:pk>', UserProfileView.as_view(), name='profile'),
    path('logout/', logout, name='logout'),
]