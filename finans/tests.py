from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from .models import Expense, Income


class FinanceViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="testpass123",
        )
        self.client.force_login(self.user)

    def test_list_shows_user_income_and_expense(self):
        Income.objects.create(
            user=self.user,
            amount="1250.00",
            category="Salary",
            description="Monthly salary",
        )
        Expense.objects.create(
            user=self.user,
            amount="42.50",
            category="Groceries",
            description="Food shopping",
        )

        response = self.client.get(reverse("list_in_view"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salary")
        self.assertContains(response, "1250.00")
        self.assertContains(response, "Groceries")
        self.assertContains(response, "42.50")

    def test_create_income(self):
        response = self.client.post(
            reverse("income_create"),
            {
                "amount": "500.00",
                "category": "Salary",
                "description": "New salary",
            },
        )

        self.assertRedirects(response, reverse("list_in_view"))
        self.assertTrue(Income.objects.filter(user=self.user, category="Salary").exists())

    def test_create_expense(self):
        response = self.client.post(
            reverse("expanse_create"),
            {
                "amount": "25.00",
                "category": "Food",
                "description": "Lunch",
            },
        )

        self.assertRedirects(response, reverse("list_in_view"))
        self.assertTrue(Expense.objects.filter(user=self.user, category="Food").exists())

    def test_update_income(self):
        income = Income.objects.create(
            user=self.user,
            amount="100.00",
            category="Old",
            description="Old description",
        )

        response = self.client.post(
            reverse("income_update", args=[income.pk]),
            {
                "amount": "150.00",
                "category": "New",
                "description": "New description",
            },
        )

        self.assertRedirects(response, reverse("list_in_view"))
        income.refresh_from_db()
        self.assertEqual(income.category, "New")
        self.assertEqual(income.amount, 150)

    def test_update_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount="10.00",
            category="Old",
            description="Old description",
        )

        response = self.client.post(
            reverse("expanse_update", args=[expense.pk]),
            {
                "amount": "20.00",
                "category": "New",
                "description": "New description",
            },
        )

        self.assertRedirects(response, reverse("list_in_view"))
        expense.refresh_from_db()
        self.assertEqual(expense.category, "New")
        self.assertEqual(expense.amount, 20)

    def test_delete_income(self):
        income = Income.objects.create(
            user=self.user,
            amount="100.00",
            category="Salary",
            description="Salary",
        )

        response = self.client.post(reverse("income_delete", args=[income.pk]))

        self.assertRedirects(response, reverse("list_in_view"))
        self.assertFalse(Income.objects.filter(pk=income.pk).exists())

    def test_delete_expense(self):
        expense = Expense.objects.create(
            user=self.user,
            amount="10.00",
            category="Food",
            description="Lunch",
        )

        response = self.client.post(reverse("expanse_delete", args=[expense.pk]))

        self.assertRedirects(response, reverse("list_in_view"))
        self.assertFalse(Expense.objects.filter(pk=expense.pk).exists())

    def test_user_cannot_edit_another_users_income(self):
        another_user = User.objects.create_user(
            username="another",
            password="testpass456",
        )
        income = Income.objects.create(
            user=another_user,
            amount="100.00",
            category="Private",
            description="Private income",
        )

        response = self.client.get(reverse("income_update", args=[income.pk]))

        self.assertEqual(response.status_code, 404)
