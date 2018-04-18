from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import IndexView, LogoutView, RegistrationView, LoginView, ApiView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('registration', RegistrationView.as_view(), name='registration'),
    path('api/v1/reviews', csrf_exempt(ApiView.as_view()), name='reviews_api_endpoint')
]
