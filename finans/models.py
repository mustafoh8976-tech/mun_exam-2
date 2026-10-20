from django.contrib.auth.models import User
from django.db import models

INCOME_CATEGORIES = [
    ('salary', 'Зарплата'),
    ('freelance', 'Подработка'),
    ('gift', 'Подарок'),
    ('investment', 'Инвестиции'),
    ('other', 'Другое'),
]

EXPENSE_CATEGORIES = [
    ('food', 'Еда'),
    ('transport', 'Транспорт'),
    ('home', 'Жильё'),
    ('entertainment', 'Развлечения'),
    ('health', 'Здоровье'),
    ('other', 'Другое'),
]


class Income(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='income')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=INCOME_CATEGORIES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)


class Expense(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=100, choices=EXPENSE_CATEGORIES)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)