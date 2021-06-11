# OSCARINE-API

[![CircleCI](https://img.shields.io/circleci/build/github/oscarine/oscarine-api?label=CircleCI%20Build&style=for-the-badge)](https://circleci.com/gh/oscarine/oscarine-api)

## Quickstart

*This project uses [Poetry](https://python-poetry.org/docs/#installation) for managing and installing Python dependencies, make sure you have it installed. After that, you can run the following commands to bootstrap your development environment*

* `git clone https://github.com/oscarine/oscarine-api`
* `cd oscarine-api`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `poetry install`
* `cp .env.example .env`
* `uvicorn app.main:app --reload`


*From now, commands starting with `$` are shell commands, `#` for SQL commands and `//` for explanatory comments*

## Setup Postgresql
*Run the following commands to setup your database*

* First download and install the postgresql database
```text
$ sudo apt-get update

$ sudo apt-get install postgresql postgresql-contrib libssl-dev
```
* Now create the database. For that we first open the psql shell. Go to the directory where your postgres file is stored
```text
// For linux users
$ sudo -u postgres psql

// For macOS users
$ psql -d postgres
```
* Create database `oscarine_db` with owner `oscarine`
```text
# CREATE USER oscarine WITH PASSWORD 'password';

# CREATE DATABASE oscarine_db WITH OWNER oscarine;
```
* Now make user `oscarine` SUPERUSER
```text
# ALTER USER oscarine WITH SUPERUSER;
```
* Now we need extension called `postgis` (install it from [here](https://postgis.net/install/))
* We can now create this extension for our database `oscarine_db`
```text
// Get inside `oscarine_db` shell
$ sudo -u postgres psql -d oscarine_db

# CREATE EXTENSION postgis;

// Now verify postgis extension
# SELECT postgis_full_version();
```
* Now, inside our project directory we can run migrations using alembic
```text
$ alembic upgrade head
```
* If you have not followed the above commands exactly please edit the `.env` file accordingly. 

## During Development
* Install pre-commit at `.git/hooks/pre-commit`
```text
$ pre-commit install
```
* We can autogenerate revision file whenever we change the database schema
```text
$ alembic revision --autogenerate -m "Your revision message"
```
* Then we can apply those changes to the database
```text
$ alembic upgrade head
```


*For contributing to Oscarine-API, please fork the project first and then clone your fork.*