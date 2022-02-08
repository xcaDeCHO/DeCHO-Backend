from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_cause, name="create_cause"),
    path('causes/', views.list_causes, name="list_causes"),
    path('view/<address>/', views.check_balances, name="check_balances"),
    path('fund_all/', views.fund_all_wallets, name="fund_all_wallets")
]
