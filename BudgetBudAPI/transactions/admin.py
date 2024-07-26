from django.contrib import admin
from .models import Transaction, CategoryType, AccountType

admin.site.register(Transaction)
admin.site.register(CategoryType)
admin.site.register(AccountType)
