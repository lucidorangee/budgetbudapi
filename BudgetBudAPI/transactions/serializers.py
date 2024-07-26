from rest_framework import serializers
from .models import Transaction, CategoryType, AccountType

class CategoryTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryType
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        return CategoryType.objects.create(user=user, **validated_data)

class AccountTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AccountType
        fields = ['id', 'name']

    def create(self, validated_data):
        user = self.context['request'].user
        return AccountType.objects.create(user=user, **validated_data)

class TransactionSerializer(serializers.ModelSerializer):
    category = CategoryTypeSerializer()
    account = AccountTypeSerializer()

    class Meta:
        model = Transaction
        fields = ['id', 'name', 'amount', 'category', 'account', 'date']
