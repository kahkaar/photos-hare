# Photos Hare

`/ˈfəʊtəʊz heə/` is an image sharing web-application created as the course project for [Tietokannat ja web-ohjelmointi `TKT20019`](https://studies.helsinki.fi/kurssit/opintojakso/otm-f15d8b61-6e3e-47d2-8191-43a92d7d8607/TKT20019?cpId=hy-lv-76)

## Features

- Coming soon.

## Running the Application

- Start a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```

- Install requirements
```bash
pip install -r requirements.txt
```

- Initialize database
```bash
sqlite3 database.db < db/schema.sql
sqlite3 database.db < db/init.sql
```

- In addition for dummy data use
```bash
sqlite3 databases.db < db/dummy.sql
```

## Evaluation

- [Kurssin arvostelu](https://hy-tikawe.github.io/materiaali/arvostelu/)
- [Tekninen tarkastuslista](https://hy-tikawe.github.io/materiaali/lista/)
