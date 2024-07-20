from django.urls import path
from .views import signup_api

app_name = 'accounts'

urlpatterns = [
    path('signup/', signup_api, name='signup'),

]