# Photos Hare

`/ˈfəʊtəʊz heə/` is an image sharing web-application created as the course project for [Tietokannat ja web-ohjelmointi `TKT20019`](https://studies.helsinki.fi/kurssit/opintojakso/otm-f15d8b61-6e3e-47d2-8191-43a92d7d8607/TKT20019?cpId=hy-lv-76)


## Table of Contents
- [Photos Hare](#photos-hare)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Running the Application](#running-the-application)
  - [Developing the Application](#developing-the-application)
  - [Running Pylint](#running-pylint)
  - [Large Dataset](#large-dataset)
  - [Development Information](#development-information)
  - [Evaluation](#evaluation)


## Features

- [X] User
  - [X] Create user
  - [X] Log in as user
  - [X] Update user settings
    - [X] Change display name capitalization
    - [X] Change password

- [X] Posting
  - [X] Share an image
    - [X] With a title
    - [X] With a description
    - [X] With tag
  - [X] Allow unlisting of posts (does not show on main page or profile page)
  - [X] Allow editing of posts
    - [X] Description
    - [X] Unlisted
    - [X] Tag
  - [X] Allow removing of posts
  - [X] Allow liking of posts

- [ ] Comments
  - [X] Create comments on posts
  - [ ] ~~Allow editing and removing of comments~~
  - [X] Allow liking of comments

- [X] Searching
  - [X] Search by post title
  - [X] Search by tag

- [X] Paginator
  - [X] Paging posts
  - [X] Paging users
  - [X] Paging comments

- [X] Seeding
  - [X] Users
  - [X] Posts
  - [X] Comments


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

1. Be within the virtual environment with developer requirements installed (detailed in [Developing the Application](#developing-the-application))

2. Run the linter (check [`.pylintrc`](/.pylintrc) for ignored files and directories)
```bash
# pylint ./
pylint ./ --disable=C0114,C0116 # These hide docstring errors
```

- [C0114 (missing-module-docstring)](https://sprytnyk.github.io/pylint-errors/plerr/errors/basic/C0114)
- [C0116 (missing-function-docstring)](https://sprytnyk.github.io/pylint-errors/plerr/errors/basic/C0116)


## Large Dataset

1. Be within the virtual environment with `Flask` installed and initialize the database (first three steps of [Running the Application](#running-the-application))

2. See the dataset sizes and other information in file [`seed.py`](./seed.py)

3. Run `seed.py`
```bash
python3 seed.py
```

Example output:
```
Generating 10000 users...
Generated 10000 users in 0.0 s
Inserting 10000 users in batches of 5000...
Inserted 10000 users in 0.13 s
Fetching 10000 user_ids and shuffling...
Retrieved 10000 shuffled user_ids in 0.01 s
Generating 100000 posts...
Generated 100000 posts in 0.09 s
Inserting 100000 posts in batches of 5000...
Inserted 100000 posts in 2.16 s
Fetching 100000 post_ids and shuffling...
Retrieved 100000 shuffled post_ids in 0.06 s
Generating 1000000 post likes...
Generated 1000000 likes in 1.06 s
Inserting 1000000 post likes in batches of 5000...
Inserted 1000000 post likes in 15.86 s
Generating 100000 comments...
Generated 100000 comments in 0.09 s
Inserting 100000 comments in batches of 5000...
Inserted 100000 comments in 1.77 s
Fetching 100000 comment_ids and shuffling...
Retrieved 100000 shuffled comment_ids in 0.06 s
Generating 1000000 post likes...
Generated 1000000 likes in 1.02 s
Inserting 1000000 comment likes in batches of 5000...
Inserted 1000000 comment likes in 15.78 s
Committing and closing the database connection...
Time spent committing and closing the database connection: 4.94 s
```


## Development Information

- Developed and tested with [`Python 3.13.3`](https://www.python.org/downloads/release/python-3133/) and [`Python 3.13.7`](https://www.python.org/downloads/release/python-3137/)

- `sqlite3` versions used with development and testing [`3.46.1`](https://sqlite.org/releaselog/3_46_1.html), [`3.49.2`](https://sqlite.org/releaselog/3_49_2.html), [`3.50.4`](https://sqlite.org/releaselog/3_50_4.html)


## Evaluation

- [Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/)
- [Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/)
