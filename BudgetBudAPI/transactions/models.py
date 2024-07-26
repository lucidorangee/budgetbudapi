from django.db import models
from django.contrib.auth.models import User

class CategoryType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class AccountType(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.ForeignKey(CategoryType, on_delete=models.SET_NULL, null=True)
    account = models.ForeignKey(AccountType, on_delete=models.SET_NULL, null=True)
    date = models.DateField()

    def __str__(self):
        return self.name
