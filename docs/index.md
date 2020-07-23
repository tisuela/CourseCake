---
layout: page
title: index
---

# CourseCake - Our Aim
At the end of the day all courses are... Courses. Every college course shares similar attributes: instructors, course name, units, etc. Therefore, we aim to create an API to access course data, where each college course shares the same basic, expected data. By making course data easier to responsibly access and more "edible" for programs, we hope CourseCake gives a responsible and smooth approach to build useful tools for students.

There are two main features to CourseCake to accomplish this goal:
- RESTful API [coursecake.tisuela.com](http://coursecake.tisuela.com)
- Installable Scraper package



## UC Irvine -- Zot your courses easier and responsibly
The motivation of CourseCake is to make it easier to develop tools like AntPlanner and Antscoper, and promote a responsible use of WebSoc by not abusing its resources.

All of the latest scraped data is stored in a local database, which avoids congesting WebSoc and allows successful requests even when WebSoc is down.

Endpoints that do directly query WebSoc are ratelimited and follow usage rates similar to other UCI Irvine course helper wesbites.


## What is a Course?

Here is an example response from our online Flask API endpoint. Full documentation available [here](https://github.com/nananananate/CourseCake/wiki/RESTful-API-Documentation)
```
{
  "courses": [
    {
      "code": "01020",
      "department": "Art",
      "departmentTitle": "Art",
      "enrolled": 72,
      "instructor": "MAJOLI, M.BORNSTEIN, J.",
      "location": "VRTL REMOTE",
      "max": 160,
      "name": "Art 1A",
      "requested": 0,
      "restrictions": "",
      "school": "Claire Trevor School of the Arts",
      "status": "NewOnly",
      "time": "TBA",
      "title": "ART IN CONTEXT",
      "type": "Lec",
      "units": 4,
      "waitlisted": 0
    }
  ]
}
```



# Documentation

[RESTful API ](https://github.com/nananananate/CourseCake/wiki/RESTful-API-Documentation)

[Scrapers](https://github.com/nananananate/CourseCake/wiki/Scrapers-Documentation)


## Installation

#### Clone repository
`git clone https://github.com/nananananate/CourseScraper`

#### Create Python virtual environment

There are a good amount of depencies for this project -- it will be good practice to use a virtual environment, albeit not necessary.

On macOS and Linux:
`python3 -m virtualenv env`

On Windows:
`py -m venv env`
The second argument is the location to create the virtual environment. Generally, you can just create this in your project and call it env.


#### Activate virtual encironment
On macOS and Linux:
`source env/bin/activate`

On Windows Command Line:
`.\env\Scripts\activate.bat`

One Windows Powershell
`.\env\Scripts\activate.ps1`

#### Navigate to the repository folder and install packages
`python -m pip install -r requirements.txt`



## Deploy Flask Application locally


#### Run flask
For Linux and Mac:

```
export FLASK_APP=coursecake/flaskapp
export FLASK_ENV=development
flask run
```

For Windows cmd, use set instead of export:

```
set FLASK_APP=coursecake/flaskapp
set FLASK_ENV=development
flask run
```

For Windows PowerShell, use $env: instead of export:

```
$env:FLASK_APP = "coursecake/flaskapp"
$env:FLASK_ENV = "development"
flask run
```

You’ll see output similar to this:

```
* Serving Flask app "coursecake/flaskapp"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```
donezo

# Future features
- Support for more complicated queries
- More comprehensive university information on departments, course prerequisites, restricts, etc.
- HTTPS only
- IF ANYONE WANTS TO HELP LEMME KNOW PLSSSS ty
