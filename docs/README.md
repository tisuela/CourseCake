# [CourseCake](http://docs.coursecake.tisuela.com/)
![Python application](https://github.com/nananananate/CourseCake/workflows/Python%20application/badge.svg) [![Coverage Status](https://coveralls.io/repos/github/nananananate/CourseCake/badge.svg?branch=master&service=github)](https://coveralls.io/github/nananananate/CourseCake?branch=master)

From developing a course planner to simply finding in-person classes, there's an easier, responsible, and more powerful way to get your university's course information.

We aim to create an API to access course data, where each college's course is unified under one schema. By making course data easier to responsibly access and more "edible" for programs, we hope CourseCake gives a smooth approach to build useful tools for students.

There are two main features to CourseCake to accomplish this goal:
- RESTful API [coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1) - [docs](https://docs.coursecake.tisuela.com/RESTful-API)
- Installable Scraper package - [docs](https://docs.coursecake.tisuela.com/Scrapers)



## UC Irvine -- Zot your courses easier and responsibly
Currently the only supported school in CourseCake, the motivation of CourseCake is to make it easier to develop tools like AntPlanner and Antscoper, and promote a responsible use of WebSoc by not abusing its resources.

All of the latest scraped data is stored in a local database, which avoids congesting WebSoc and allows successful requests even when WebSoc is down.

Endpoints that do directly query WebSoc are ratelimited and follow usage rates similar to other UCI Irvine course helper wesbites.

## What is a Course?
Here is an example response using one of our `courses` endpoints. Full documentation available [here](http://docs.coursecake.tisuela.com/RESTful-API).
The response is a dictionary containing a list of `course` objects. The schema of a `course` is shown in this example.


```
{
  "courses": [
    {
      "building": "string",
      "code": "string",
      "department": "string",
      "departmentTitle": "string",
      "enrolled": 0,
      "instructor": "string",
      "location": "string",
      "max": 0,
      "name": "string",
      "requested": 0,
      "restrictions": "string",
      "room": "string",
      "school": "string",
      "status": "string",
      "time": "string",
      "title": "string",
      "type": "string",
      "units": 0,
      "updated": "datetime: string,null",
      "waitlisted": 0
    }
  ]
}
```



# Documentation

[RESTful API ](http://docs.coursecake.tisuela.com/RESTful-API)

[Scrapers](http://docs.coursecake.tisuela.com/Scrapers)


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
- More comprehensive university information on departments, course prerequisites, restricts, etc.
- Prerequisite mapping to create a network of classes (along with a node graph GUI)
- HTTPS only
- IF ANYONE WANTS TO HELP LEMME KNOW PLSSSS ty
