from django.db.models import Q
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from django_filters import rest_framework as filters, CharFilter
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

from .models import Budget, Income, Expense, Category
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    BudgetSerializer,
    IncomeSerializer,
    ExpenseSerializer,
    CategorySerializer,
    BudgetShareSerializer,
)


class BudgetFilter(filters.FilterSet):
    name = CharFilter(lookup_expr="icontains")

    class Meta:
        model = Budget
        fields = ["name", "owner"]


class BudgetViewSet(viewsets.ModelViewSet):
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BudgetFilter

    def get_queryset(self):
        return Budget.objects.filter(
            Q(owner=self.request.user) | Q(shared_with=self.request.user)
        ).distinct()

    def retrieve(self, request, *args, **kwargs):
        budget = self.get_object()
        serializer = self.get_serializer(budget)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=["POST", "DELETE"])
    def share_on_off(self, request, *args, **kwargs):
        budget = self.get_object()
        serializer = BudgetShareSerializer(data=request.data)
        if serializer.is_valid() and (
            serializer.validated_data["shared_with"] != self.request.user
        ):
            if self.request.method == "POST":
                budget.shared_with.add(serializer.validated_data["shared_with"])
                budget.save()
                return Response({"status": "budget shared"})
            else:
                budget.shared_with.remove(serializer.validated_data["shared_with"])
                budget.save()
                return Response({"status": "budget no longer shared"})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class IncomeViewSet(viewsets.ModelViewSet):
    serializer_class = IncomeSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Income.objects.filter(
            Q(budget__owner=self.request.user)
            | Q(budget__shared_with=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data["budget"].owner:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(
            Q(budget__owner=self.request.user)
            | Q(budget__shared_with=self.request.user)
        ).distinct()

    def perform_create(self, serializer):
        if self.request.user == serializer.validated_data["budget"].owner:
            serializer.save()
        else:
            raise PermissionDenied("You do not have permission to perform this action.")


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
