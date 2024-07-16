from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="categories")

    def __str__(self):
        return self.name


class Budget(models.Model):
    name = models.CharField(max_length=100)
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="owned_budgets"
    )
    shared_with = models.ManyToManyField(User, related_name="shared_budgets")

    def __str__(self):
        return self.name


class Income(models.Model):
    budget = models.ForeignKey(Budget, on_delete=models.CASCADE, related_name="incomes")
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"


class Expense(models.Model):
    budget = models.ForeignKey(
        Budget, on_delete=models.CASCADE, related_name="expenses"
    )
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return f"{self.category} - {self.amount}"
