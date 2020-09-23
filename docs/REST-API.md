---
title: REST API
---
 [![Website coursecake.tisuela.com](https://img.shields.io/website?label=Web%20API&up_color=success&up_message=up&url=https%3A%2F%2Fcoursecake.tisuela.com)](https://coursecake.tisuela.com/)

**[coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)**

You can check out [CourseCake online](https://coursecake.tisuela.com)!

* Try out our [REST](http://coursecake.tisuela.com/api/v1) or [GraphQL](http://coursecake.tisuela.com/api/graphql) endpoint.
* Take a look at comprehensive documentation [here](http://coursecake.tisuela.com)


## [GraphQL](http://coursecake.tisuela.com/api/graphql) - Beyond REST
[coursecake.tisuela.com/api/graphql](http://coursecake.tisuela.com/api/graphql) is another Web API endpoint (it is not RESTful) for queries via GraphQL.

[GraphQL](https://graphql.org/) is a query language for APIs. It allows for more dynamic, specific queries, helping CourseCake give you the information you need. However, the kind of requests you will have to make are more complex.

You can see our GraphQL Schema documentation and **try it out live** on our [GraphiQL browser](http://coursecake.tisuela.com/api/graphql).  

New to GraphQL? Learn more on their website: [graphql.org](https://graphql.org/)

## Course vs Class
📚 A `Course` is a unit of teaching that lasts a term.

📝 A `Class` is an offering of a `Course`. This means a `Class` has information for the purpose of enrollment and meaning, such as  instructor, meeting times, location, and status (open or closed). A `Course` has many `classes`, however each `Class` belongs to exactly one `Course`.


### Course Schema
📚 This defines a `Course` as a response from our REST API and GraphQL Web API, the model in `database.models`, and the class in `scrapers.course`.
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

### Class Schema
📝 This defines a `Class` as a response from our REST API and GraphQL Web API, the model in `database.models`, and the class (renamed `CourseClass`) in `scrapers.course_class`.

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

## REST API Endpoints
🌐 `/api/v1`

[Full documentation](https://coursecake.tisuela.com)

[Try it out!](https://coursecake.tisuela.com/api/v1)

### All courses
📚 `GET /courses/all/<university>`

Returns all courses from a university.
`university` is determined by their domain.edu.

### Search Courses
🔍 `GET courses/search/<university>`

Query our database for courses


#### Create complex queries
🔬 All parameter names can be followed by [filter].
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
"id" | Course id, like DANCE 101
"units" |
"department" | See Department codes on your school's Course Schedule
"title" | Readable name, like Intro to Dance


Here's a request that returns all of UCI's in-person classes taught on Monday, Wednesday, and Friday which are not taught by Professor Badprof
```
GET coursecake.tisuela.com/api/v1/classes/search/uci?location[notlike]=line,remote,tba&time[like]=mwf&instructor=goodprof
```



## Can't find what you are looking for?
The comprehensive documentation (less readable) can be found [here](http://coursecake.tisuela.com):
[coursecake.tisuela.com](http://coursecake.tisuela.com)


## API Examples

### Python
```
import requests

# URL to the Search API endpoint
url = "http://coursecake.tisuela.com/api/v1/courses/search/uci"    

# search parameters for the GET request
search_params = {
    "department[like]": "compsci",
    "title[not]": "intro to bad course",
    "units": "4"
}

# send request
response = requests.get(url, params=search_params)

# view body of response
print(response.text)
```

## Try it out!
Try out our API using Swagger UI [here](http://coursecake.tisuela.com/api/v1):
[coursecake.tisuela.com/api/v1](http://coursecake.tisuela.com/api/v1)
