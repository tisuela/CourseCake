---
title: REST API
---
## [coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)
You can check out CourseCake online! [Try out our REST API](http://coursecake.tisuela.com/api/v1) or look at comprehensive [documentation](http://coursecake.tisuela.com/api/v1) [here](http://coursecake.tisuela.com/api/v1)


## GraphQL
[coursecake.tisuela.com/api/graphql](http://coursecake.tisuela.com/api/graphql) is another Web API endpoint (it is not RESTful) for GraphQL.

[GraphQL](https://graphql.org/) is a query language for APIs. It allows for more dynamic, specific queries, helping CourseCake give you the information you need. However, the kind of requests you will have to make are more complex. You can see our GraphQL Schema documentation and try it out live on our [GraphiQL browser](http://coursecake.tisuela.com/api/graphql).  

New to GraphQL? Learn more on their website: https://graphql.org/

## `Course` vs `Class` -- What's the Difference?
A `Course` is a unit of teaching that lasts a term.

A `Class` is an offering of a `Course`. This means a `Class` has information for the purpose of enrollment and meaning, such as  instructor, meeting times, location, and status (open or closed). A `Course` has many `classes`, however each `Class` belongs to exactly one `Course`.


### `Course` Schema
This defines a `Course` as a response from our REST API and GraphQL Web API, the model in `coursecake.database.models`, and the class in `coursecake.scrapers.course`.
s
Below is an example:
```
{
  "course_id": "string",
  "title": "string",
  "department": "string",
  "units": 4,
  "prerequisites_str": "string",
  "department_title": "string",
  "restrictions": "string",
  "school": "string",
  "university_name": "UCI",
  "term_id": "FALL-2020-1"
}

```

### `Class` Schema
This defines a `Class` as a response from our REST API and GraphQL Web API, the model in `coursecake.database.models`, and the class (renamed `CourseClass`) in `coursecake.scrapers.course_class`.

Looking at our source code, you see names like `CourseClass` or `a_class`. This naming prevents collisions with each other and with the python-built in blueprint for objects: `class`.

Below is an example:
```
{
  "class_id": "string",
  "course_id": "string",
  "instructor": "string",
  "time": "string",
  "location": "string",
  "building": "string",
  "room": "string",
  "status": "string",
  "type": "string",
  "units": 4,
  "max": 0,
  "enrolled": 0,
  "waitlisted": 0,
  "requested": 0,
  "university_name": "UCI",
  "term_id": "FALL-2020-1",
  "updated": "2019-08-24T14:15:22Z"
}
```

The breakdown of a course from the JSON response is analogous to the definition of a `Course` in `coursecake/scrapers/course.py`:

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
