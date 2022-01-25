from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_cause, name="create-cause"),
    path('causes/', views.list_causes, name="list-causes"),
    path('view/<address>', views.check_balances, name="check-balances")
]