from django.urls import path
from .views import signup_api, signup_clear

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_api, name='signup'),
    path('signup-clear/',signup_clear, name='signup-clear'),

]