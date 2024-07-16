from rest_framework import viewsets, permissions
from django_filters import rest_framework as filters, CharFilter
from .models import Budget, Income, Expense, Category
from .serializers import (
    BudgetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    CategorySerializer,
)


class BudgetFilter(filters.FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Budget
        fields = ["name", "owner"]


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BudgetFilter

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user) | Budget.objects.filter(
            shared_with=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(
            budget__owner=self.request.user
        ) | Income.objects.filter(budget__shared_with=self.request.user)


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            budget__owner=self.request.user
        ) | Expense.objects.filter(budget__shared_with=self.request.user)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]
