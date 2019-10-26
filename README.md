# OSCARINE-API
*API to be consumed by Oscarine android and web clients*

## Quickstart
*Run the following commands to bootstrap your development environment*

* `git clone https://github.com/Haider8/oscarine-api`
* `cd oscarine-api`
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
* Now create the database. For that we first open the psql shell. Go the directory where your postgres file is stored.
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
* If you have not followed the above commands exactly or your owner, database name is different please edit the `.env` file accordingly. 

> For contributing to Oscarine-API, please fork the project first and then clone your fork.