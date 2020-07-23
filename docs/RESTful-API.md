---
title: RESTful API
---
## [coursecake.tisuela.com/api](https://coursecake.tisuela.com/api)
We are now online! For the next several days, we will be making revisions continuously, so we apologize if the service is down. Do be sure to refresh this page daily as needed -- API improvements will be posted.


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
"waitlisted" | int

## API Endpoints `/api`

### All courses `/uci/courses/all`
Returns all UCI courses

### Search Courses `/uci/courses/search`
Query our database for courses

Here are the supported search parameters:
Parameter | Value | Comments
--- | --- | ---
"code" | String | Search by course code (returns one course)
"department" | String | Search by department with matching code (See department codes on WebSoc)
"instructor" | String | Search by instructor containing this string
"units" | String or int | Search courses with matching units
"building" | String | Search by building 
"notlocation" | String | Excludes courses in buildings/room containing this string
"notinstructor" | String  | Excludes courses whos instructor contains this string

Usage:
```
/api/uci/courses/search?instructor=pattis&units=4&department=compsci

/api/uci/courses/search?notinstructor=badprof&notlocation=badlocation
```

### Live Search Courses `/uci/courses/live-search`
Queries courses retrieved directly from the university's course scheduling website.
Same usage as `/uci/courses/search`.

Here are the supported search parameters:

Parameter | Value | Comments
--- | --- | ---
"code" | String | Unique to every `Course`
"department" | String | Check your university's department codes      
"instructor" | String | Staff/professors/teachers
"breadth" | String | GE requirement (ex: GE-2)
"starttime" | String | (ex: 8:00am)
"endtime" | String | (ex: 8:00am)
"title" | String | alternative to course name
"units" | String or int | We show the highest units possible for a course

Parameter | Value | Comments
--- | --- | ---
"code" | String | Search by course code (returns one course)
"department" | String | Search by department with matching code (See department codes on WebSoc)
"instructor" | String | Search by instructor containing this string
"units" | String or int | Search courses with matching units
"building" | String | Search by building 
"notlocation" | String | Excludes courses in buildings/room containing this string
"notinstructor" | String  | Excludes courses whos instructor contains this string

You must specify one of the following parameters: `code`, `department`, `instructor`, or `breadth`.

## API Examples

### Python
```
import requests

# URL to the Search API endpoint
url = "http://coursecake.tisuela.com/api/uci/courses/search"    

# search parameters for the GET request
searchParams = {
    "department": "compsci",
    "notinstructor": "badprof",
    "units": "4"
}

# send request
response = requests.get(url, params=searchParams)

# view body of response
print(response.text)
```
