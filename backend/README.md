# Backend

Backend Flask project for MTG project.

[Flask docs](https://flask.palletsprojects.com/en/3.0.x/).

### Prerequisites

To run the API, first make sure you have `python` installed. We are using Python 3.12 and a virtual environment with `pipenv`. You may have to downgrade or upgrade.

```bash
# check python version
python --version
```

Also make sure you have Pipenv and Flask installed and the environment activated:

```bash
# install pipenv
pip install pipenv

# install Flask (note the uppercase F)
pip install Flask

# sync the dependencies
pipenv sync

# activate the environment
pipenv shell
```

Before starting the backend, you need to initialize the database. Make sure you have Postgres installed locally and can run `psql`.

First, go into a Postgres session:

```bash
psql
```

Initialize a database with the name `dis_magic`, a user with the name `admin` and a password called `password`:

```bash
postgres=# CREATE DATABASE dis_magic;
postgres=# CREATE USER admin WITH PASSWORD 'password';
postgres=# GRANT ALL PRIVILEGES ON DATABASE dis_magic TO admin;
postgres=# \c dis_magic postgres
postgres=# GRANT ALL ON SCHEMA public TO admin;
```

Verify the database was initialized with:

```bash
postgres=# \l
```

Next, you need to run the initialization of the DB that also seeds the database with the data we are using. Before doing so, download the sample data from [this link](https://data.scryfall.io/default-cards/default-cards-20240513090527.json), name it `rawCards.json` and put it inside `data/rawCards.json`. Then run:

```bash
python init_db.py
```

### Developing

To start the api, run:

```bash
flask run --debug
```

This should start the server on [localhost:5000](http://localhost:5000).