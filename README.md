# CourseCake - Our Aim
At the end of the day all courses are... Courses. Every college course shares similar attributes: instructors, course name, units, etc. Therefore, we aim to scrape college course website to create an API where all course data can be accessed, where each college course shares the same basic, expected data.

By making course data easier to access and more "edible" for programs, we hope CourseCake gives a smoother approach build useful tools for students.

## What is a Course?
Here is an example response from our online Flask API endpoint
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

The breakdown of a course from the JSON response is analogous to the definition of a `Course` in `coursecake/scrapers/course.py`:

Key/Attribute | Value
--- | ---
"code" | String
"department" | String       
"departmentTitle" | String
"enrolled" | String
"instructor" | String
"location" | String
"max" | int
"name" | String
"requested" | int
"restrictions" | String
"school" | String
"status" | String
"time" | String
"title" | String
"type" | String
"units" | int
"waitlisted" | int`





## UC Irvine -- Zot your courses easier and responsibly
CourseCake was inspired to make it easier to develop tools like AntPlanner and Antscoper.

All of the latest scraped data is stored in a local database, which avoids congesting WebSoc and does not

Also, UCI's WebSoc is kinda... ugly. With the course information, I plan to make something useful. Idk what that is yet lol


## Installation

#### Clone repository
`git clone https://github.com/nananananate/CourseScraper`

#### Navigate to the repository folder and install packages
`pip install -r requirements.txt`


## Using the Scrapers Package
Within the cloned repository:
```
from coursecake.scrapers.course_scraper import CourseScraper
```

From CourseScraper, you can load all UCI courses
```
scraper = CourseScraper()
courses = scraper.getAllUCICourses()
```
Courses are loaded in chunks; it will take a minute for all courses to be collected.

`courses` is a list of `Course` objects, ad defined in `coursecake/scrapers/course.py`. From the `Course` object, you can get obtain the course's data.

Here is an example of printing some course data from `courses`
```
for course in courses:

  # This does not print out all attributes, just a select few to avoid clutter
  # see more in Course.__str__(self)
  print(course)

  # print the status of the course; if it is open, closed, full, etc.
  print(course.status)
```

To save all UCI courses into a JSON file:
```
scraper.downloadUCICourses()
```

The format of data within the JSON file is close to identical with the online endpoint of CourseCake; see the above heading `What is a Course` for an example.


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
