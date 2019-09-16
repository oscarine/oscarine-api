# OSCARINE-API

## Project installation instructions locally (for development and contribution)

* Firstly you have to fork this project.
* Then, clone this project using the command ```https://github.com/[YOUR USERNAME]/oscarine-api.git```. Use your own GitHub username.
* Now ```cd``` into ```oscarine-api```.
* Now set up your virtual environment for this project using the command ```python3 -m venv venv```. We are using Python3.6.
* Activate your newly created virtual environment using ```source venv/bin/activate```.
* Now to install the required dependencies run ```pip install -r requirements.txt```.
* To setup your database run this command now ```flask db upgrade```. This will create the sqlite database ```app.db``` in your root directory.
* Create a ```.env``` file in the project's root directory.
* Finally, run the project using ```flask run```.

##### To start the server in development mode, add this in your `.env` file:
```text
FLASK_ENV=development
```

## Some documentations which may come in handy

* [Flask](https://flask.palletsprojects.com/en/1.1.x/)
* [Flask-SQLAlchemy](https://flask-sqlalchemy.palletsprojects.com/en/2.x/)
* [Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)
* [Flask-Login](https://flask-login.readthedocs.io/en/latest/)