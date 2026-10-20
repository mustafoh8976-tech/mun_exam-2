from django.contrib import admin

from .models import Expense, Income


@admin.register(Income)
class IncomeAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("description",)


@admin.register(Expense)
class ExpenseAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "amount", "category", "created_at")
    list_filter = ("category",)
    search_fields = ("description",)
