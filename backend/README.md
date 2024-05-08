# Backend

Backend Flask project for MTG project.

[Flask docs](https://flask.palletsprojects.com/en/3.0.x/).

### Prerequisites

To run the API, first make sure you have `python` installed. We are using Python 3.11 and a virtual environment with `pipenv`.

```bash
# check python version
python -v
```

Also make sure you have Pipenv installed and the environment activated:

```bash
# install pipenv
pip install pipenv

# sync the dependencies
pipenv sync

# activate the environment
pipenv shell
```

### Developing

To start the api, run:

```bash
flask run
```

This should start it on [localhost:5000](http://localhost:5000). If not, try installing flask.