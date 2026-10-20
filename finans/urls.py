from django.urls import path

from . import views

urlpatterns = [
    path("", views.list_in_view, name="list_in_view"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("income/", views.income_list_view, name="income_list"),
    path("income/create/", views.create_income_view, name="income_create"),
    path("income/<int:pk>/update/", views.update_income_view, name="income_update"),
    path("income/<int:pk>/delete/", views.income_delete_view, name="income_delete"),
    path("expenses/", views.expanse_list_view, name="expanse_list"),
    path("expenses/create/", views.create_expanse_view, name="expanse_create"),
    path("expenses/<int:pk>/update/", views.update_expanse_view, name="expanse_update"),
    path("expenses/<int:pk>/delete/", views.expanse_delete_view, name="expanse_delete"),
    path("summary_income/", views.summary_income_view, name="summary_income"),
    path("summary_expense/", views.summary_expense_view, name="summary_expense"),
    path("summary/", views.summary_view, name="summary"),
]
