# Photos Hare

`/ˈfəʊtəʊz heə/` is an image sharing web-application created as the course project for [Tietokannat ja web-ohjelmointi `TKT20019`](https://studies.helsinki.fi/kurssit/opintojakso/otm-f15d8b61-6e3e-47d2-8191-43a92d7d8607/TKT20019?cpId=hy-lv-76)

## Features

- [X] User
  - [X] Create user
  - [X] Log in as user
  - [X] Update user settings (change password, and display name capitalization)

- [ ] Posting
  - [X] Share an image
    - [X] With a title
    - [X] With a description
    - [ ] With tags
  - [X] Allow unlisting of posts (does not show on main page or profile page)
  - [ ] Allow editing of posts (title, description, unlisted, tags)
  - [X] Allow removing of posts
  - [ ] Allow liking of posts

- [ ] Comments
  - [X] Create comments on posts
  - [ ] Allow editing and removing of comments
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

4. Create a secret key in `config.py` (see `config.template.py`)

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

## Evaluation

- [Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/)
- [Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/)
