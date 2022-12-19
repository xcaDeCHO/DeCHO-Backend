from django.urls import path

from . import views

urlpatterns = [
    # All Endpoints
    path("create/", views.create_cause, name="create_cause"),
    path("causes/", views.list_causes, name="list_causes"),
    path("causes/<int:id>/", views.detail_cause, name="detail_cause"),
    path("view/<address>/", views.check_balances, name="check_balances"),
    path("null_causes/", views.null_causes, name="null_causes"),
    path("giveaway/", views.giveaway, name="store_giveaway_addresses"),
    path("results/", views.results, name="giveaway_results"),
    path("transactions/<int:cause_id>/<address>/", views.get_user_donations_to_cause, name="get+user_donations_cause")
    # path("fund_all/", views.fund_all_wallets, name="fund_all_wallets"),
]
