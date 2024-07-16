from rest_framework import viewsets, permissions
from .models import Budget
from .serializers import (
    BudgetSerializer,
)


class BudgetViewSet(viewsets.ModelViewSet):
    queryset = Budget.objects.all()
    serializer_class = BudgetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(owner=self.request.user) | Budget.objects.filter(
            shared_with=self.request.user
        )

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
