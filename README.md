# CourseCake - Our Aim
At the end of the day all courses are... Courses. Every college course shares similar attributes: instructors, course name, units, etc. Therefore, we aim to scrape college course website to create an API where all course data can be accessed, where each college course shares the same basic, expected data.

By making course data easier to access and more "edible" for programs, we hope CourseCake gives a smoother approach build useful tools for students.

## What is a Course?
Our API defines a course as:
```
{
  code: String
  name: String        # formal name, like CS 121
  title: String       # more readable name, like Intro to Informatics
  department: String
  instructor: String
  location: String
  units: int

}
```


## UC Irvine -- Zot your courses easier and responsibly
CourseCake was inspired to make it easier to develop tools like AntPlanner and Antscoper. 

To avoid congesting UCI's WebSoc, all queries are directed to a local database, not WebSoc. We scrape the latest data for you!

Also, UCI's WebSoc is kinda... ugly. With the course information, I plan to make something useful. Idk what that is yet lol


## Deploy Flask Application locally
#### Clone repository
`git clone https://github.com/nananananate/CourseScraper`

#### Navigate to the repository folder and install packages
`pip install -r requirements.txt`

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
