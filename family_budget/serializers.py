from rest_framework import serializers
from .models import Budget, Income, Expense, Category
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "user"]


class IncomeSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Income
        fields = ["id", "budget", "category", "amount", "date"]


class ExpenseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Expense
        fields = ["id", "budget", "category", "amount", "date"]


class BudgetSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    shared_with = UserSerializer(many=True, read_only=True)
    incomes = IncomeSerializer(many=True, read_only=True)
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = Budget
        fields = ["id", "name", "owner", "shared_with", "incomes", "expenses"]
