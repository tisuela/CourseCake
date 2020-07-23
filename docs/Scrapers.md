---
title: Scrapers
---
CourseCake is sliced (haha get it?) into two parts -- a standalone scraper package `coursecake.scrapers`, and a web app package `coursecake.flaskapp` built on top of the scraper package.

This section will cover the usability of the standalone scraper package.

## CourseScraper `coursecake.scrapers.course_scraper`
`CourseScraper` is the main class in which you can access all scraper classes and their functions -- you should not have to import any of the other scrapers.

The long term plan -- IF this project continues -- is to have support for multiple universities by having a scraper for each university. Currently, only UC Irvine is supported. Regardless, this is the motivation behind the `scrapers` module, to only have to import a few classes for complete usability (`CourseScraper`, `Scraper`, and `Course`).

Thus, `CourseScraper` has methods to return a university's specific `Scraper`, so you don't have to make an import for that specific school.

Importing CourseScraper:
```
from coursecake.scrapers.course_scraper import CourseScraper
```

### Get University's Scraper `CourseScraper.getUciScraper() -> Scraper`
Returns UC Irvine's specific scraper. All specific scrapers inherit from the Scraper class, so for usability, the expected return value is a `Scraper` object (although a `UciScraper` object would also be valid and more specific).

From this `Scraper` object you can return all of the university's courses, query specific courses, save the courses to a file, etc. All information returned from this `Scraper` object comes from the university's course schedule website -- it will be the latest data and you need internet connection to allow the `Scraper` to make requests to their website.

## Scraper `coursecake.scrapers.scraper`


### Get all courses `Scraper.scrape() -> dict`

Loads all of the university's courses for the latest term as a dictionary of `Course`, with their course code as the key. Each course is accessible by their key -- their course code (a String).

For any university, this `.scrape()` will take around a minute to complete, since it must iterate over several pages of courses from the course schedule website to collect all courses.
 
Example usage:
```
scraper = CourseScraper().getUciScraper()
courses = scraper.scrape()
```

### Search specific courses `Scraper.getCourses(args: dict) -> dict`

Get the latest course information (directly scraped from web) on courses fulfilling search criteria. Returns results as a dictionary of `Course`, with their course code as the key
`args` is a `dict` in which you specify search parameters and their values. Keys and value formats are the same throughout all universities (currently only one, UC Irvine lol)

Here are the currently supported arguments: 

Key | Value
--- | ---
"code" | String
"department" | String       
"instructor" | String
"breadth" | String
"starttime" | String (ex: 8:00am)
"endtime" | String (ex: 8:00am)
"title" | String
"units" | String or int

You must specify one of the following parameters: `code`, `department`, `instructor`, or `breadth`

Example usage:
```
args = {
  "department': "compsci",
  "units": 4
  }

scraper = CourseScraper().getUciScraper()
courses = scraper.getCourses(args)
```




## Course `coursecake.scrapers.course`
A `Course` object holds all information you can get on a course, accessible by attributes (ex: `Course.instructor`).
You can easily serialize a `Course` using `Course.__dict__`

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

The format of data within the JSON file is a dictionary of `Course.__dict__`, where `Course.code` are the keys.
