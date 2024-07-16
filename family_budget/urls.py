from rest_framework.routers import DefaultRouter
from .views import BudgetViewSet, IncomeViewSet, ExpenseViewSet, CategoryViewSet

router = DefaultRouter()
router.register(r"budgets", BudgetViewSet, basename='Budget')
router.register(r"incomes", IncomeViewSet, basename='Income')
router.register(r"expenses", ExpenseViewSet, basename='Expense')
router.register(r"categories", CategoryViewSet, basename='Category')

urlpatterns = router.urls
