# Pylint report

This report was made using the following snippet `pylint ./ --disable=C0114,C0116`. This was done, because I did not intend on using docstrings for the project, thus not needing to show these in the report. However, I have given the absolute output of `pylint ./` in [`pylint-report.raw.txt`](./pylint-report.raw.txt) if you are interested.

Also, some files and directories were excluded from this report, which you can see in [`.pylintrc`](./.pylintrc). These ignores were made to reduce the clutter in the final report (no need to lint files within `.venv`, etc...). I also added `seed.py` to the ignore list because I assume, we are only linting the code that was produced for the application itself, not testing/seeding files.

- [Pylint report](#pylint-report)
  - [The report](#the-report)
  - [Analysis](#analysis)
    - [W0613: Unused argument 'e' (unused-argument)](#w0613-unused-argument-e-unused-argument)
    - [W0102: Dangerous default value \[\] as argument (dangerous-default-value)](#w0102-dangerous-default-value--as-argument-dangerous-default-value)
    - [W0622: Redefining built-in 'type' (redefined-builtin)](#w0622-redefining-built-in-type-redefined-builtin)
    - [R0912: Too many branches (14/12) (too-many-branches)](#r0912-too-many-branches-1412-too-many-branches)
    - [W0622: Redefining built-in 'set' (redefined-builtin)](#w0622-redefining-built-in-set-redefined-builtin)
    - [R0801: Similar lines in 2 files](#r0801-similar-lines-in-2-files)

## The report

As said earlier, this linting report was made with the following snippet to avoid docstrings `pylint ./ --disable=C0114,C0116`.

```bash
************* Module app
app.py:29:23: W0613: Unused argument 'e' (unused-argument)
************* Module db
db.py:26:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
db.py:38:0: W0102: Dangerous default value [] as argument (dangerous-default-value)
************* Module api.comments
api/comments.py:98:27: W0622: Redefining built-in 'type' (redefined-builtin)
************* Module api.posts
api/posts.py:356:27: W0622: Redefining built-in 'type' (redefined-builtin)
************* Module routes.post
routes/post.py:178:4: W0622: Redefining built-in 'type' (redefined-builtin)
************* Module routes.user
routes/user.py:155:0: R0912: Too many branches (14/12) (too-many-branches)
************* Module routes.helpers.alert
routes/helpers/alert.py:14:0: W0622: Redefining built-in 'set' (redefined-builtin)
************* Module routes.helpers.session
routes/helpers/session.py:48:0: W0622: Redefining built-in 'set' (redefined-builtin)
************* Module routes.helpers.__init__
routes/helpers/__init__.py:1:0: R0801: Similar lines in 2 files
==api.posts:[183:192]
==api.users:[102:111]
  p.unlisted,
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM (duplicate-code)
routes/helpers/__init__.py:1:0: R0801: Similar lines in 2 files
==api.posts:[74:82]
==api.users:[130:138]
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM (duplicate-code)
routes/helpers/__init__.py:1:0: R0801: Similar lines in 2 files
==api.posts:[47:55]
==api.users:[103:111]
  SUM(
    CASE
      WHEN pl.type = TRUE THEN 1
      WHEN pl.type = FALSE THEN -1
      ELSE 0
    END
  ) AS likes
FROM (duplicate-code)
routes/helpers/__init__.py:1:0: R0801: Similar lines in 2 files
==api.posts:[84:89]
==api.users:[140:145]
  LEFT JOIN posts_likes AS pl ON p.id = pl.post_id
WHERE
  p.unlisted = FALSE
  AND u.username = LOWER(?)
GROUP BY (duplicate-code)

------------------------------------------------------------------
Your code has been rated at 9.83/10 (previous run: 9.83/10, +0.00)
```

## Analysis

### W0613: Unused argument 'e' (unused-argument)

- `app.py:29:23: W0613: Unused argument 'e' (unused-argument)`

Flask always returns a parameter on error handlers, thus there needed to be a parameter to make it work. Kept with `e` to look the same as the other error handlers, however, it could have been an `_` which would tell the developer that it is not used.


### W0102: Dangerous default value [] as argument (dangerous-default-value)

- `db.py:26:0: W0102: Dangerous default value [] as argument (dangerous-default-value)`
- `db.py:38:0: W0102: Dangerous default value [] as argument (dangerous-default-value)`


The code does not do change the list after calling the function, also the list is not used after it being executed, thus this should not actually be dangerous.


### W0622: Redefining built-in 'type' (redefined-builtin)

- `api/comments.py:98:27: W0622: Redefining built-in 'type' (redefined-builtin)`
- `api/posts.py:356:27: W0622: Redefining built-in 'type' (redefined-builtin)`
- `routes/post.py:178:4: W0622: Redefining built-in 'type' (redefined-builtin)`

Not using the built-in 'type' anywhere in the codebase and I did not find a better variable (and table column) name for this.


### R0912: Too many branches (14/12) (too-many-branches)

- `routes/user.py:155:0: R0912: Too many branches (14/12) (too-many-branches)`

This was needed for giving the user information on what happened on errors, thus the 14 branches.


### W0622: Redefining built-in 'set' (redefined-builtin)

- `routes/helpers/alert.py:14:0: W0622: Redefining built-in 'set' (redefined-builtin)`
- `routes/helpers/session.py:48:0: W0622: Redefining built-in 'set' (redefined-builtin)`

The `set` functions in `alert` and `session` will not be used without the former part. Only being used as `alert.set()` or `session.set()` (I have renamed my `session` as `sesh` in import clauses to prevent conflicts with the `session` from `Flask`).


### R0801: Similar lines in 2 files

- `routes/helpers/__init__.py:1:0: R0801: Similar lines in 2 files`

These are SQL queries, so similarities are unavoidable.
