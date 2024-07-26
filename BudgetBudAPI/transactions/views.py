from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Transaction, CategoryType, AccountType
from .serializers import TransactionSerializer, CategoryTypeSerializer, AccountTypeSerializer
from rest_framework.permissions import IsAuthenticated
from django.conf import settings
import openai

class TransactionListCreateView(generics.ListCreateAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['category', 'account', 'date']
    search_fields = ['name']
    ordering_fields = ['date', 'amount']

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class TransactionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user)

class CategoryTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = CategoryTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CategoryType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CategoryTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategoryTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return CategoryType.objects.filter(user=self.request.user)

class AccountTypeListCreateView(generics.ListCreateAPIView):
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccountType.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class AccountTypeRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = AccountTypeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AccountType.objects.filter(user=self.request.user)

class TransactionAIAnalysisView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, transaction_id=None):
        user = request.user

        if transaction_id:
            # Analyze a specific transaction
            try:
                transaction = Transaction.objects.get(id=transaction_id, user=user)
                transaction_list = [transaction]
            except Transaction.DoesNotExist:
                return Response({"error": "Transaction not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            # Analyze all transactions for the user
            transaction_list = Transaction.objects.filter(user=user)
        
        transaction_data = list(transaction_list.values('name', 'amount', 'category__name', 'account__name', 'date'))

        # Prepare the data to be sent to OpenAI
        transaction_summary = self.prepare_summary(transaction_data)

        # Call OpenAI API
        openai.api_key = settings.OPENAI_API_KEY
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an expert financial analyst."},
                {"role": "user", "content": f"Analyze the following transactions: {transaction_summary}"}
            ],
            max_tokens=150
        )

        return Response({'analysis': response.choices[0].message['content']})

    def prepare_summary(self, transaction_list):
        summary = ""
        for transaction in transaction_list:
            summary += (f"Transaction: {transaction['name']}, Amount: {transaction['amount']}, "
                        f"Category: {transaction['category__name']}, Account: {transaction['account__name']}, "
                        f"Date: {transaction['date']}\n")
        return summary