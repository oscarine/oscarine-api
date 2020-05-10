# OSCARINE-API

## Quickstart
*Run the following commands to bootstrap your development environment*

* `git clone https://github.com/oscarine/oscarine-api`
* `cd oscarine-api`
* `python3 -m venv venv`
* `source venv/bin/activate`
* `pip install -r requirements/dev.txt`
* `cp .env.example .env`
* `uvicorn app.main:app --reload`

## Setup Postgresql
*Run the following commands to setup your database*

* First download and install the postgresql database
```text
sudo apt-get update
sudo apt-get install postgresql postgresql-contrib libssl-dev
```
* Now create the database. For that we first open the psql shell. Go to the directory where your postgres file is stored
```text
# For linux users
sudo -u postgres psql

# For macOS users
psql -d postgres
```
* Create database `oscarine_db` with owner `oscarine`
```text
CREATE USER oscarine WITH PASSWORD 'password';
CREATE DATABASE oscarine_db WITH OWNER oscarine;
```
* After that we can run migrations using alembic
```text
alembic upgrade head
```
* If you have not followed the above commands exactly please edit the `.env` file accordingly. 

## During Development
* We can create a revision file whenever we change the database schema
```text
alembic revision -m "Your revision message"
```


> For contributing to Oscarine-API, please fork the project first and then clone your fork.