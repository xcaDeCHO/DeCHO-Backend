from Decho.celery import app
from .models import Cause
from .utils import check__choice_balance
from celery import shared_task



@app.task
def update_cause_status():
    causes = Cause.objects.filter(status='pending')
    for cause in causes:
        address = cause.decho_wallet.address
        balance = check__choice_balance(address)
        try:
            balance = int(balance)
        except:
            return

        if balance/100 >= cause.cause_approval.goal:
            cause.status = 'Approved'



