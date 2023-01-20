from .common import *
import django_heroku

# for digital ocean setup

DEBUG = True

ALLOWED_HOSTS = ["decho-mainnet.herokuapp.com", "app.decho.finance"]

HUEY = {
    "huey_class": "huey.RedisHuey",  # Huey implementation to use.
    "name": "Decho",  # Use db name for huey.
    'url': config('REDIS_URL'),
    "results": True,  # Store return values of tasks.
    "store_none": False,  # If a task returns None, do not save to results.
    "immediate": False,  # If DEBUG=True, run synchronously.
    "utc": True,  # Use UTC for all times internally.
    "blocking": True,  # Perform blocking pop rather than poll Redis.
    "consumer": {
        "workers": 1,
        "worker_type": "thread",
        "initial_delay": 0.1,  # Smallest polling interval, same as -d.
        "backoff": 1.15,  # Exponential backoff using this rate, -b.
        "max_delay": 10.0,  # Max possible polling interval, -m.
        "scheduler_interval": 1,  # Check schedule every second, -s.
        "periodic": True,  # Enable crontab feature.
        "check_worker_health": True,  # Enable worker health checks.
        "health_check_interval": 1,  # Check worker health every second.
    },
}
CHOICE_ID = 722955559
ALGOD_ADDRESS = "https://node.algoexplorerapi.io"
INDEXER_ADDRESS = "https://algoindexer.algoexplorerapi.io"
ALGOD_CLIENT = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, {"X-API-Key": ""})
INDEXER_CLIENT = indexer.IndexerClient(ALGOD_TOKEN, INDEXER_ADDRESS, {"X-API-Key": ""})
django_heroku.settings(locals())
