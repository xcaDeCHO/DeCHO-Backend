from django.urls import path

from . import views

urlpatterns = [
    path("create/", views.create_cause, name="create_cause"),
    path("causes/", views.list_causes, name="list_causes"),
    path("causes/<int:id>", views.detail_cause, name="detail_cause"),
    path("view/<address>/", views.check_balances, name="check_balances"),
    path("null_causes/", views.null_causes, name="null_causes"),
    path("giveaway/", views.giveaway, name="store_giveaway_addresses"),
    path("results/", views.results, name="giveaway_results")
    # path("fund_all/", views.fund_all_wallets, name="fund_all_wallets"),
]
