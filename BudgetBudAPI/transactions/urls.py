from django.urls import path
from .views import (
    TransactionListCreateView, TransactionRetrieveUpdateDestroyView,
    CategoryTypeListCreateView, CategoryTypeRetrieveUpdateDestroyView,
    AccountTypeListCreateView, AccountTypeRetrieveUpdateDestroyView,
    TransactionAIAnalysisView
)

urlpatterns = [
    path('transactions/askai/', TransactionAIAnalysisView.as_view(), name='transaction-ai-analysis'),
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionRetrieveUpdateDestroyView.as_view(), name='transaction-detail'),
    path('categories/', CategoryTypeListCreateView.as_view(), name='category-list-create'),
    path('categories/<int:pk>/', CategoryTypeRetrieveUpdateDestroyView.as_view(), name='category-detail'),
    path('accounts/', AccountTypeListCreateView.as_view(), name='account-list-create'),
    path('accounts/<int:pk>/', AccountTypeRetrieveUpdateDestroyView.as_view(), name='account-detail'),
]
