from decimal import Decimal

from django.contrib.auth.models import User
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Budget, Category, Income, Expense


class BudgetAPITests(APITestCase):
    fixtures = ["initial_data.json"]

    def setUp(self):
        self.client = APIClient()
        self.budget_1_id = Budget.objects.get(pk=1).id
        self.category_1_id = Category.objects.get(pk=1).id

    def test_create_budget(self):
        self.client.login(username="user1", password="user1pass")
        response = self.client.post("/api/budgets/", {"name": "Annual Budget"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Budget.objects.count(), 4)
        self.assertEqual(Budget.objects.latest('id').name, "Annual Budget")

    def test_view_shared_budget(self):
        self.client.login(username="user2", password="user2pass")
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 2)
        self.assertEqual(response.data["results"][0]["name"], "Monthly Budget")

    def test_view_budget_incomes_and_expenses(self):
        self.client.login(username="user1", password="user1pass")
        response = self.client.get(f"/api/budgets/{self.budget_1_id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["incomes"]), 1)
        self.assertEqual(len(response.data["expenses"]), 1)
        self.assertEqual(response.data["incomes"][0]["amount"], "3000.00")
        self.assertEqual(response.data["expenses"][0]["amount"], "500.00")

    def test_add_income_to_budget(self):
        self.client.login(username="user1", password="user1pass")
        response = self.client.post(
            "/api/incomes/",
            {
                "budget": self.budget_1_id,
                "category": self.category_1_id,
                "amount": "2000.00",
                "date": "2023-07-15",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Income.objects.count(), 4)
        self.assertEqual(Income.objects.latest('id').amount, Decimal("2000.00"))

    def test_add_expense_to_budget(self):
        self.client.login(username="user1", password="user1pass")
        response = self.client.post(
            "/api/expenses/",
            {
                "budget": self.budget_1_id,
                "category": self.category_1_id,
                "amount": "300.00",
                "date": "2023-07-15",
            },
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Expense.objects.count(), 4)
        self.assertEqual(Expense.objects.latest('id').amount, Decimal("300.00"))

    def test_filter_budgets_by_name(self):
        self.client.login(username="user1", password="user1pass")
        Budget.objects.create(name="Weekly Budget", owner=User.objects.get(pk=1))
        response = self.client.get("/api/budgets/", {"name": "weekly"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["name"], "Weekly Budget")

    def test_pagination(self):
        self.client.login(username="user1", password="user1pass")
        for i in range(15):
            Budget.objects.create(name=f"Budget {i}", owner=User.objects.get(pk=1))
        response = self.client.get("/api/budgets/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data["results"]), 10)  # Default PAGE_SIZE is 10
        response = self.client.get("/api/budgets/?page=2")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            len(response.data["results"]), 7
        )  # 5 more budgets plus the original two
