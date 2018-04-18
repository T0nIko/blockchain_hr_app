from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    email = models.EmailField()
    first_name = models.TextField()
    last_name = models.TextField()


class EthAccount(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='eth_account'
    )

    address = models.TextField()
    p_key = models.TextField()


class ContractInstance(models.Model):
    contract_instance_adress = models.TextField()
    reviewer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='reviews'
    )
    targer = models.ForeignKey(
        User,
        on_delete=models.PROTECT,
        related_name='targeted_reviews'
    )