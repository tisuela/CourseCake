# [![CourseCake](https://github.com/nananananate/CourseCake/blob/master/docs/coursecake_header.png?raw=true)](https://docs.coursecake.tisuela.com/)
![Build](https://github.com/nananananate/CourseCake/workflows/Python%20application/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/nananananate/CourseCake/badge.svg?branch=master)](https://coveralls.io/github/nananananate/CourseCake?branch=master)  [![Website coursecake.tisuela.com](https://img.shields.io/website?label=Web%20API&up_color=success&up_message=up&url=https%3A%2F%2Fcoursecake.tisuela.com)](https://coursecake.tisuela.com/) ![last commit](https://img.shields.io/github/last-commit/nananananate/CourseCake) ![commits activity](https://img.shields.io/github/commit-activity/m/nananananate/CourseCake)

There are three main features CourseCake offers that make university course information more "edible" for developers:
- 🌐 Web API (REST + GraphQL) [coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1) - [docs](https://docs.coursecake.tisuela.com/REST-API)
- 💾 Database package - [docs](http://docs.coursecake.tisuela.com/Database)
- 🔍 Scraper package - [docs](https://docs.coursecake.tisuela.com/Scrapers)

CourseCake aims to create an API to access course data, where college course information is unified by our schemas. By making course 📚 data easier to responsibly access and more "edible" 🍰 for developers, we hope CourseCake gives a smooth approach to build useful tools for students.

## 🐜 UC Irvine -- Zot your courses easier and responsibly
Currently the only supported school in CourseCake, the motivation of CourseCake is to make it easier to develop tools like AntPlanner and Antscoper, and promote a responsible use of WebSoc by not abusing its resources.

All of the latest scraped data is stored in a local database, which avoids congesting WebSoc and allows successful requests even when WebSoc is down.

Endpoints that do directly query WebSoc are ratelimited and follow usage rates similar to other UCI Irvine course helper websites.

## 📚 Course vs 📝 Class -- What's the Difference?
A `Course` is a unit of teaching that lasts a term.

A `Class` is an offering of a `Course`. This means a `Class` has information for the purpose of enrollment and meaning, such as  instructor, meeting times, location, and status (open or closed). A `Course` has many `classes`, however each `Class` belongs to exactly one `Course`.

See more about `Course` and `Class`, such as their schemas, in the documentation below ⬇

# Documentation

[Web API](http://docs.coursecake.tisuela.com/REST-API)

[Database](http://docs.coursecake.tisuela.com/Database)

[Scrapers](http://docs.coursecake.tisuela.com/Scrapers)


## Installation

#### 👩‍👧 Clone repository
```
git clone https://github.com/nananananate/CourseCake
cd CourseCake
```

#### 🐍 Create Python virtual environment

There are a good amount of depencies for this project -- it will be good practice to use a virtual environment, albeit not necessary.

On macOS and Linux:
`python3 -m virtualenv env`

On Windows:
`python -m venv env`
The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.


#### ✅ Activate virtual environment
On macOS and Linux:
`source env/bin/activate`

On Windows Command Line:
`.\env\Scripts\activate.bat`

One Windows Powershell
`.\env\Scripts\activate.ps1`

#### 📦 Navigate to the repository folder and install packages
`python -m pip install -r requirements.txt`



### 🏃‍♀️ Deploy Fast API Application locally
We are no longer using Flask!

#### 🦄 Run Fast API using uvicorn

Install uvicorn if you haven't already (if you followed the previous step correctly, you should be gucci.
```
python -m pip install uvicorn
```

Run uvicorn.
```
uvicorn coursecake.fastapi_app.main:app --reload
```

You’ll see output similar to this:

```
←[32mINFO←[0m:     Uvicorn running on ←[1mhttp://127.0.0.1:8000←[0m (Press CTRL+C to quit)
←[32mINFO←[0m:     Started reloader process [←[36m←[1m38240←[0m] using ←[36m←[1mstatreload←[0m
←[32mINFO←[0m:     Started server process [←[36m13020←[0m]
←[32mINFO←[0m:     Waiting for application startup.
←[32mINFO←[0m:     Application startup complete.
```
donezo

# Future features
- Seperation of the Course Schema into a smaller Course Schema and a Class Schema. A Class is an offering of a Course (watch me name things to avoid name collisions haha)
- Implementing a GraphQL endpoint using Graphene.
- Prerequisite mapping to create a network of classes (along with a node graph GUI) via Neo4j (probably in seperate repository).
- IF ANYONE WANTS TO HELP LEMME KNOW PLSSSS ty

[![GitHub license](https://img.shields.io/github/license/nananananate/CourseCake.svg)](https://github.com/nananananate/CourseCake/blob/master/LICENSE)
