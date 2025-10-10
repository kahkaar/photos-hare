# Photos Hare

`/ˈfəʊtəʊz heə/` is an image sharing web-application created as the course project for [Tietokannat ja web-ohjelmointi `TKT20019`](https://studies.helsinki.fi/kurssit/opintojakso/otm-f15d8b61-6e3e-47d2-8191-43a92d7d8607/TKT20019?cpId=hy-lv-76)


## Table of Contents
- [Photos Hare](#photos-hare)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Running the Application](#running-the-application)
  - [Developing the Application](#developing-the-application)
  - [Running Pylint](#running-pylint)
  - [Development Information](#development-information)
  - [Evaluation](#evaluation)


## Features

- [X] User
  - [X] Create user
  - [X] Log in as user
  - [X] Update user settings
    - [X] Change display name capitalization
    - [X] Change password

- [ ] Posting
  - [X] Share an image
    - [X] With a title
    - [X] With a description
    - [ ] With tag
  - [X] Allow unlisting of posts (does not show on main page or profile page)
  - [ ] Allow editing of posts
    - [ ] ~~Title~~
    - [X] Description
    - [X] Unlisted
    - [ ] Tag
  - [X] Allow removing of posts
  - [ ] Allow liking of posts

- [ ] Comments
  - [X] Create comments on posts
  - [ ] ~~Allow editing and removing of comments~~
  - [ ] Allow liking of comments

- [ ] Searching
  - [X] Posts
  - [ ] Comments


## Running the Application

1. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install [Flask](https://pypi.org/project/Flask/)
```bash
pip install Flask
```

3. Initialize the database
```bash
sqlite3 database.db < schema/schema.sql
sqlite3 database.db < schema/init.sql
```

4. Create a secret key in `config.py` (see [`config.template.py`](/config.template.py))

5. Start the server using Flask
```bash
flask run
```

## Developing the Application

1. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install developer requirements
```bash
pip install -r dev.requirements.txt
```

3. Initialize the database
```bash
sqlite3 database.db < schema/schema.sql
sqlite3 database.db < schema/dummy.sql
```

4. Create a secret key in `config.py` (see [`config.template.py`](/config.template.py))

5. Start the server in **debug mode**
```bash
flask run --debug
```


## Running Pylint

1. Be within the virtual environment with developer requirements installed detailed in [Developing the Application](#developing-the-application)

2. Run the linter (check [`.pylintrc`](/.pylintrc) for ignored directories)
```bash
# pylint ./
pylint ./ --disable=C0114,C0116 # These hide docstring errors
```

- [C0114 (missing-module-docstring)](https://sprytnyk.github.io/pylint-errors/plerr/errors/basic/C0114)
- [C0116 (missing-function-docstring)](https://sprytnyk.github.io/pylint-errors/plerr/errors/basic/C0116)


## Development Information

- Developed and tested with [`Python 3.13.3`](https://www.python.org/downloads/release/python-3133/) and [`Python 3.13.7`](https://www.python.org/downloads/release/python-3137/)

- `sqlite3` versions used with development and testing [`3.46.1`](https://sqlite.org/releaselog/3_46_1.html), [`3.49.2`](https://sqlite.org/releaselog/3_49_2.html), [`3.50.4`](https://sqlite.org/releaselog/3_50_4.html)


## Evaluation

- [Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/)
- [Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/)
