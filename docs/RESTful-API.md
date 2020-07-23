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
"enrolled" | int
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

### All courses `GET /uci/courses/all`
Returns all UCI courses

### Search Courses `GET /uci/courses/search`
Query our database for courses

You can search for multiple values for a parameter by separating them with commas:
```
/uci/courses/search?units=4,8
```

Here are the supported search parameters:

Parameter | Matching behavior | Description
--- | --- | ---
"code" | Exact | Course Code
"building" | Exact | 
"room" | Exact |
"status" | Exact | full, open, etc.
"units" | Exact |
"department" | Exact | See Department codes on your school's Course Schedule
"notbuilding" | Excludes exact
"notinstructor" | Excludes exact
"notroom" | Excludes exact
"nottunits" | Excludes exact
"instructor" | Contains 
"name" | Contains | Formal name, like DANCE 101
"title" | Contains | Readable name, like Intro to Dance
"time" | Contains 
"location" | Contains 
"nottime" | Excludes contains
"notlocation" | Excludes contains


Here's a request that returns all of UCI's in-person classes taught on Monday, Wednesday, and Friday which are not taught by Professor Badprof
```
GET coursecake.tisuela.com/api/uci/courses/search?notlocation=line,remote,tba&time=mwf&notinstructor=badprof
```

### Live Search Courses `GET /uci/courses/live-search`
Queries courses retrieved directly from the university's course scheduling website.
Same usage as `/uci/courses/search`.

Here are the supported search parameters:

Parameter | Description
--- | --- 
"code" | Unique to every `Course`
"department" | Check your university's department codes      
"instructor" | Staff/professors/teachers
"breadth" | GE requirement (ex: GE-2)
"starttime" | (ex: 8:00am)
"endtime" | (ex: 8:00am)
"title" | alternative to course name
"units" | We show the highest units possible for a course


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
