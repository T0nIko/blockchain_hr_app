from django.shortcuts import render, redirect
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login

from .forms import RegistrationForm
from .models import User


class LoginMixin(LoginRequiredMixin):
    login_url = '/login'


class IndexView(View):
    template_name = 'index.html'

    def get(self, request):
        return render(
            request,
            self.template_name
        )


class LogoutView(View):
    def get(self, request):
        logout(request)

        return redirect('index')


class RegistrationView(View):
    template_name = 'registration.html'

    def get(self, request):
        return render(
            request,
            self.template_name,
            {
                'form': RegistrationForm()
            }
        )

    def post(self, request):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user_data = {
                'first_name': form.cleaned_data['fl_name'].split(' ')[0],
                'last_name': form.cleaned_data['fl_name'].split(' ')[1],
                'email': form.cleaned_data['email'],
                'username': form.cleaned_data['email'],
                'password': form.cleaned_data['password']
            }

            user, created = User.objects.get_or_create(**user_data)

            if not created:
                login(request, user)

                return redirect('index')

            return redirect('login')
        else:
            return redirect('registration')
