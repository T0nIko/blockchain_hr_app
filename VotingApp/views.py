from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login

from .forms import RegistrationForm
from .models import User, EthAccount, ContractInstance
from .utils import contract_instance_wrapper, post_review

from eth_account import Account

import json


def assign_eth_account(user):
    user_eth_account = Account.create()

    eth_account = EthAccount(
        user=user,
        address=user_eth_account.address,
        p_key=user_eth_account.privateKey
    )

    eth_account.save()


def render_json(d, status=200):
    return HttpResponse(json.dumps(d), content_type='application/json', status=status)


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


class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        return render(request, self.template_name)


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
            else:
                assign_eth_account(user)

            return redirect('login')
        else:
            return redirect('registration')


class ApiView(View):
    def get(self, request):
        data = [
            contract_instance_wrapper(
                obj.contract_instance_adress
            )
            for obj in ContractInstance.objects.all()
        ]

        return render_json(
            {
                'reviews': data
            }
        )

    def post(self, request):
        params = json.loads(request.body)

        print(User.objects.last().eth_account.address)
        if params['type'] == 'add':
            contract_address = post_review(
                User.objects.get(id=params['review']['reviewer_id']).eth_account,
                User.objects.get(id=params['review']['target_id']).eth_account,
                params['review']['text'],
                params['review']['is_positive']
            )

            review_contract = ContractInstance(
                contract_instance_adress=contract_address,
                reviewer_id=params['review']['reviewer_id'],
                targer_id=params['review']['target_id']
            )
            review_contract.save()

            return render_json(
                {
                    'msg': 'ok'
                }
            )
        elif params['type'] == 'user_reviews':
            contracts_addresses = [
                contract.contract_instance_adress
                for contract in ContractInstance.objects.filter(
                    reviewer_id=params['user']['id']
                )
            ]

            data = [
                contract_instance_wrapper(contract_address)
                for contract_address in contracts_addresses
            ]

            return render_json(
                {
                    'data': data
                }
            )
        elif params['type'] == 'user_reviewed':
            contracts_addresses = [
                contract.contract_instance_adress
                for contract in ContractInstance.objects.filter(
                    targer_id=params['user']['id']
                )
            ]

            data = [
                contract_instance_wrapper(contract_address)
                for contract_address in contracts_addresses
            ]

            return render_json(
                {
                    'data': data
                }
            )

        return render_json(
            {
                'msg': 'Unable to determine request type.'
            }
        )
