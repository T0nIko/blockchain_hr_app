from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.views import LoginView

from .views import IndexView, LogoutView, RegistrationView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('registration', RegistrationView.as_view(), name='registration')
]
