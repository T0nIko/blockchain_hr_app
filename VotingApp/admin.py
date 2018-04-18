from django.contrib import admin

from .models import User, EthAccount, ContractInstance

admin.site.register(User)
admin.site.register(EthAccount)
admin.site.register(ContractInstance)
