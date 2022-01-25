from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_cause, name="createcause"),
    path('causes/', views.list_causes, name="list_causes"),
    path('view/<address>', views.check_balances, name="check_balances")
]