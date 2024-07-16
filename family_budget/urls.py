from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, IncomeViewSet, ExpenseViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet)
router.register(r"incomes", IncomeViewSet)
router.register(r"expenses", ExpenseViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = router.urls
