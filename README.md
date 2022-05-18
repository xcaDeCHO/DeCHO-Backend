# DeCHO-Backend

## _To run on Local_
* Navigate to the Project Directory
* Activate a Python virtual environment
* run `pip install -r requirements.txt` in terminal
* create an env file that follows env.example in your project root

[comment]: <> (* run `celery -A Decho beat` )
* Open another terminal and run `python manage.py runserver`

The Project should be up and running at this point



## Running tests on local (recommended to test this on the dev(testnet) branch)
* Make sure molotov is installed by running `pip install -r requirements.txt`
* Go to folder containing `tests.py` and run `molotov -w 10 -p 4 -d 2 -x tests.py`
* This will spin up 100 workers and run the test
* Sucesses shouldn't exceed the specified limits in `settings/common.py`