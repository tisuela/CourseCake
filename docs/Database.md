---
title: Database
---
You can programatically upload and query courses from the database.

The `coursecake.database` package uses `sqlalchemy` to insert, update, and query courses from the local `sqlite` database.

## Upload courses
`coursecake.database` uses `coursecake.scrapers` to scrape courses for insertion into the database.
