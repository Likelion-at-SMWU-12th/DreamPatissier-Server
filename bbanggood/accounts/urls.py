from django.urls import path
from .views import signup_api, signup_clear, login_api, logout_api

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_api, name='signup'),
    path('signup-clear/',signup_clear, name='signup-clear'),
    path('login/', login_api, name='login'),
    path('logout/',logout_api, name='logout')
]