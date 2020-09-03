---
title: Database
---

## UNDER CONSTRUCTION, SORRY
if u need info desperately, there are random comments and docstrings in the code


You can programmatically upload and query courses from the database.

The `coursecake.database` package uses [sqlalchemy](https://www.sqlalchemy.org/) to insert, update, and query courses from the local [sqlite](https://www.sqlite.org/index.html) database.

## Structure
* `database.crud` - Create, Read, Update, and Delete functions are here. The classes for dynamically creating queries (`CourseQuery` and `ClassQuery`) are here
* `database.models` - The two main models, `Course` and `Class` are defined here. All other models are here.
* `database.sql` - All connections made to the database are imported from here. Configurations for connections are defined here.
* `database.uploads` - Functions to populate the database are defined here. This is the ONLY file that talks to the `coursecake.scrapers` package.

## Upload courses & classes
`coursecake.database` uses `coursecake.scrapers` to scrape courses for insertion into the database. All upload functions are in `coursecake.database.uploads`.

Here's a script that uploads courses.
```
from coursecake.database import uploads, sql

db = sql.SessionLocal()

uploads.update_all(db)

```


## Query Courses
Queries to the `Course` table can be made dynamically from a `dictionary` using our class `CourseQuery` from `coursecake.database.crud`.

```
from coursecake.database import crud, sql

db = sql.SessionLocal()

query_params = {
    "department[like]": "compsci",
    "title[not]": "intro to bad course",
    "units": "4"
}
query = crud.CourseQuery(db, university = "uci", args = query_params)
```
