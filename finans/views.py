from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import ExpenseForm, IncomeForm, RegisterForm
from .models import EXPENSE_CATEGORIES, INCOME_CATEGORIES, Expense, Income


def register_view(request):
    if request.user.is_authenticated:
        return redirect("list_in_view")

    form = RegisterForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("list_in_view")
    return render(request, "register.html", context={"form": form, "title": "Регистрация"})


def login_view(request):
    if request.user.is_authenticated:
        return redirect("list_in_view")

    form = AuthenticationForm(request, data=request.POST or None)
    for field in form.fields.values():
        field.widget.attrs["class"] = "form-control"

    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect(request.GET.get("next") or "list_in_view")
    return render(request, "login.html", context={"form": form, "title": "Вход"})


def logout_view(request):
    if request.method == "POST":
        logout(request)
    return redirect("login")


@login_required(login_url="login")
def list_in_view(request):
    incomes = Income.objects.filter(user=request.user).order_by("-created_at")
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "list.html", context={"incomes": incomes, "expenses": expenses})


@login_required(login_url="login")
def income_list_view(request):
    incomes = Income.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "income_list.html", context={"incomes": incomes})


@login_required(login_url="login")
def create_income_view(request):
    form = IncomeForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        income = form.save(commit=False)
        income.user = request.user
        income.save()
        return redirect("list_in_view")
    return render(request, "transaction_form.html", context={"form": form, "title": "Добавить доход"})


@login_required(login_url="login")
def update_income_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)
    form = IncomeForm(request.POST or None, instance=income)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_in_view")
    return render(request, "transaction_form.html", context={"form": form, "title": "Изменить доход"})


@login_required(login_url="login")
def income_delete_view(request, pk):
    income = get_object_or_404(Income, pk=pk, user=request.user)

    if request.method == "POST":
        income.delete()
        return redirect("list_in_view")

    return render(request, "transaction_delete.html", context={"transaction": income, "title": "Удалить доход"})


@login_required(login_url="login")
def expanse_list_view(request):
    expenses = Expense.objects.filter(user=request.user).order_by("-created_at")
    return render(request, "expanse_list.html", context={"expenses": expenses})


@login_required(login_url="login")
def create_expanse_view(request):
    form = ExpenseForm(request.POST or None)

    if request.method == "POST" and form.is_valid():
        expense = form.save(commit=False)
        expense.user = request.user
        expense.save()
        return redirect("list_in_view")

    return render(
        request,
        "transaction_form.html",
        context={"form": form, "title": "Добавить расход"},
    )


@login_required(login_url="login")
def update_expanse_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)
    form = ExpenseForm(request.POST or None, instance=expense)

    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("list_in_view")

    return render(request, "transaction_form.html", context={"form": form, "title": "Изменить расход"})


@login_required(login_url="login")
def expanse_delete_view(request, pk):
    expense = get_object_or_404(Expense, pk=pk, user=request.user)

    if request.method == "POST":
        expense.delete()
        return redirect("list_in_view")

    return render(request, "transaction_delete.html", context={"transaction": expense, "title": "Удалить расход"})


@login_required(login_url="login")
def summary_income_view(request):
    incomes = Income.objects.filter(user=request.user)
    total = 0

    for income in incomes:
        total += income.amount

    sorted_categories = []

    for category, name in INCOME_CATEGORIES:
        category_total = 0
        for income in incomes:
            if income.category == category:
                category_total += income.amount

        sorted_categories.append((category_total, name))

    sorted_categories.sort(reverse=True)
    by_category = []

    for amount, name in sorted_categories:
        if amount > 0:
            by_category.append({"name": name, "total": amount})

    return render(
        request,
        "summary_detail.html",
        context={
            "title": "Сводка по доходам",
            "total": total,
            "by_category": by_category,
            "kind": "income",
        },
    )


@login_required(login_url="login")
def summary_expense_view(request):
    expenses = Expense.objects.filter(user=request.user)
    total = 0

    for expense in expenses:
        total += expense.amount

    sorted_categories = []

    for category, name in EXPENSE_CATEGORIES:
        category_total = 0
        for expense in expenses:
            if expense.category == category:
                category_total += expense.amount

        sorted_categories.append((category_total, name))

    sorted_categories.sort(reverse=True)
    by_category = []

    for amount, name in sorted_categories:
        if amount > 0:
            by_category.append({"name": name, "total": amount})

    return render(
        request,
        "summary_detail.html",
        context={
            "title": "Сводка по расходам",
            "total": total,
            "by_category": by_category,
            "kind": "expense",
        },
    )


@login_required(login_url="login")
def summary_view(request):
    incomes = Income.objects.filter(user=request.user)
    expenses = Expense.objects.filter(user=request.user)
    total_income = 0
    total_expense = 0

    for income in incomes:
        total_income += income.amount

    for expense in expenses:
        total_expense += expense.amount

    balance = total_income - total_expense

    if balance > 0:
        bonus = balance / 10
    else:
        bonus = 0

    return render(request,"summary.html",context={"total_income": total_income,"total_expense": total_expense,"balance": balance,"bonus": bonus})
