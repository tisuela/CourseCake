---
title: RESTful API
---
## [coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)
Released /api/v1
With the new release, you can try out our API or look at comprehensive documentation [here](http://coursecake.tisuela.com/api/v1)


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

## API Endpoints `/api/v1`

### All courses `GET /courses/all/<university>`
Returns all courses from a university.
`university` is determined by their domain.edu.

### Search Courses `GET courses/search/<university>`
Query our database for courses


#### Create complex queries
All parameter names can be followed by [filter].
The default filter (applied when no filter is specified) is equals

For example:
```
title[like]=dance
```

Here are all valid filters:
`like`
`notlike`
`equals`
`not`

You can search for multiple values for a parameter by separating them with commas:
```
/courses/search/<university>?units=4,8
```

Here are the supported search parameters:

Parameter |  Description
--- | ---
"code" | Course Code
"building" |
"room" | 
"status" | full, open, etc.
"units" | 
"department" | See Department codes on your school's Course Schedule
"name" | Formal name, like DANCE 101
"title" | Readable name, like Intro to Dance
"time" | 
"location" | 


Here's a request that returns all of UCI's in-person classes taught on Monday, Wednesday, and Friday which are not taught by Professor Badprof
```
GET coursecake.tisuela.com/api/uci/courses/search?location[notlike]=line,remote,tba&time[like]=mwf&instructor=goodprof
```

### Live Search Courses `GET /courses/live-search/<university>`
Queries courses retrieved directly from the university's course scheduling website.
Because this endpoint queries the live website directly, this endpoint is ratelimited and does not have the ability to create complex queries. Course data is also less comprehensive, so it is recommended to use the `search` endpoint

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


## Can't find what you are looking for?
The comprehensive documentation (less readable) can be found [here](http://coursecake.tisuela.com/api/v1):
[coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)


## API Examples

### Python
```
import requests

# URL to the Search API endpoint
url = "http://coursecake.tisuela.com/api/v1/courses/search/uci"    

# search parameters for the GET request
searchParams = {
    "department[like]": "compsci",
    "instructor[not]": "badprof",
    "units": "4"
}

# send request
response = requests.get(url, params=searchParams)

# view body of response
print(response.text)
```

## Try it out!
Try out our API using Swagger UI [here](http://coursecake.tisuela.com/api/v1):
[coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)
