# Who can contribute?
Anyone! I (the creator) am open to guiding those who are not familiar with python or the tools CourseCake uses to promote your own growth as well as the utility of this tool!

## Why should I contribute?
Particularly if you are a university student, the end goal is that this tool helps your university. We are continually designing CourseCake to be modular and easy to contribute to. You can independently or with a team implement support for your school without having to understand the entire code base.

## How can I contribute?
Check out the current [issues](https://github.com/nananananate/CourseCake/issues) that need attention.

For adding support for your school, please check out the files in [this directory](https://github.com/nananananate/CourseCake/tree/master/coursecake/scrapers), `coursecake.scrapers`. You will want to be familiar with `Course` and `CourseClass`. Documentation of `coursecake.scrapers` can be found [here](https://docs.coursecake.tisuela.com/Scrapers/). Within `coursecake.scrapers` create a folder called `your school's domain name`. However you would like to go about this, whether multiple files or just one file, create a class that will act as the public interface for support for your school.

### What does this class look like?
You can check out the other folders within `coursecake.scrapers` for examples. At the end of the day, you need a method, `.get_classes(testing: bool = False) -> dict` which returns a dictionary of `Course`. Web API and database support is easily implemented on our end, so don't worry about that (meaning, **you don't need to learn** GraphQL, SQLAlchemy, or FastAPI).
