# Photos Hare

`/ˈfəʊtəʊz heə/` is an image sharing web-application created as the course project for [Tietokannat ja web-ohjelmointi `TKT20019`](https://studies.helsinki.fi/kurssit/opintojakso/otm-f15d8b61-6e3e-47d2-8191-43a92d7d8607/TKT20019?cpId=hy-lv-76)

## Features

### Initial Features
- [ ] Create user
  - [ ] Log in as user

- [ ] Share an image with a title, a description and tags
  - [ ] Allow unlisting of posts (does not show on main page or profile page)
  - [ ] Allow editing of posts (title, description, tags)
  - [ ] Allow removing of posts
  - [ ] Allow liking of posts

- [ ] Create comments on posts
  - [ ] Allow editing and removing of comments
  - [ ] Allow liking of comments

- More features coming soon™️

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

**OR**

```bash
pip install -r requirements.txt
```

3. Initialize database
```bash
sqlite3 database.db < db/schema.sql
sqlite3 database.db < db/init.sql
```

4. Start the server using Flask
```bash
flask run
```

### Developing the Application

1. Create a virtual environment
```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install developer requirements
```bash
pip install -r dev.requirements.txt
```

3. Initialize database
```bash
sqlite3 database.db < db/schema.sql
sqlite3 database.db < db/dummy.sql
```

4. Start the server in **debug mode**
```bash
flask run --debug
```

## Evaluation

- [Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/)
- [Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/)
