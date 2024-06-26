# 🧙 Magic the Gathering'dle 🧙

Project for the course Databases and Information systems at UCPH.

### Table of Contents

1. [Description](#description)
2. [Setup](#setup)
   1. [Setting up the backend](#setting-up-the-backend)
   2. [Setting up the frontend](#setting-up-the-frontend)
3. [Running the backend and frontend simultaneously](#running-the-backend-and-frontend-simultaneously)
4. [Useful links to docs](#useful-links-to-docs)

### Description

Magic the Gathering'dle is a Wordle-inspired game where the goal is to guess a card from a subset of the ~30,000 cards. In short, you press a card and the game filters out other cards according to the traits of the guessed and correct card. The goal is to guess the correct card in as few guesses (clicks) as possible. It challenges players to strategically pick what categories of traits that filter out most cards at a time to minimize the number of guesses.

SQL expressions are used in the endpoint handlers in `app.py` and regular expressions are used in `card_parser.py` in the backend.

Read the setup below to get started.

### ER-diagram

The E/R diagram of the database structure is shown below. Note that there are some slight deviations from the names defined in the columns in the SQL tables.

![ER-diagram](./er-diagram.png)

### Setup

#### Setting up the backend

The backend is using Flask which exposes an API that our frontend consumes. First, cd into the `backend` directory.

```bash
cd backend
```

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

Verify the database was initialized by running:

```bash
postgres=# \l
```

Next, you need to run the initialization of the DB that also seeds the database with the data we are using. Before doing so, download the sample data from [this link](https://data.scryfall.io/default-cards/default-cards-20240513090527.json), name it `rawCards.json` and put it inside `data/rawCards.json`. Then run:

```bash
python init_db.py
```

This should parse the cards and seed to database with the extracted data. Before running the frontend, verify that you can run the backend by doing:

```bash
pipenv shell
flask run
```

If you encounter missing package errors, try installing the missing package with `pip install [package-name]`. Otherwise, you're now ready to setup the frontend.

#### Setting up the frontend

The frontend uses Svelte with the framework SvelteKit.

Make sure to have [Node](https://nodejs.org/en) installed.

First, cd into the frontend project:

```bash
cd frontend
```

Install dependencies:

```bash
npm install
```

Once you've created a project and installed dependencies with `npm install`, you can start the development server:

```bash
npm run dev

# or start the server and open the app in a new browser tab
npm run dev -- --open
```

That's all the setup there is. To run the fully functioning project, run the frontend and backend at the same time and navigate to [localhost:5173](http://localhost:5173/). You can use the commands detailed below for a quick way to run them simultaneously.

### Running the backend and frontend simultaneously

We have provided a few make commands to run both the frontend and the backend at the same time, as shown below.

Note that `make z` activates the virtual environment in the Flask project before running flask. We found that this was particularly useful on Windows machines as the package wouldn't be recognized as being installed globally.

```bash
# Running the frontend and the backend simultaneously
make

# Same as above if you have to activate pipenv
make z

# Running the backend
make b

# Running the frontend
make f
```

If you cannot use `make`, just run the frontend and backend seperately:

```bash
# In terminal 1
cd backend
pipenv shell
flask run --debug
```

```bash
# In terminal 2
cd frontend
npm run dev
```

Open a browser and navigate to [localhost:5173](http://localhost:5173/) to open the frontend and try the game. Have fun!

### Useful links to docs

Below is a list of links to documentation of the technologies we use.

[Flask](https://flask.palletsprojects.com/en/3.0.x/) (backend framework).

[Svelte](https://svelte.dev/docs/introduction) (frontend library).

[SvelteKit](https://kit.svelte.dev/docs/introduction) (frontend framework).

[Shadcn-svelte](https://www.shadcn-svelte.com/docs) (component library).
