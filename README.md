# CourseScraper
Scrapes course information from universities and stores them as a consistent data structure (locally).

Planning to mongodb or SQLAlchemy

## Gathering course information from UC Irvine
UCI's WebSoc is kinda... ugly. With the course information, I plan to make something useful. Idk what that is yet lol


## Deploy Flask Application locally
#### Clone repository
`git clone https://github.com/nananananate/CourseScraper`

#### Navigate to the repository folder and install packages
`pip install -r requirements.txt`

#### Run flask
For Linux and Mac:

`export FLASK_APP=coursecake/flaskapp`
`export FLASK_ENV=development`
`flask run`


For Windows cmd, use set instead of export:

`set FLASK_APP=coursecake/flaskapp`

`set FLASK_ENV=development`

`flask run`

For Windows PowerShell, use $env: instead of export:

`$env:FLASK_APP = "coursecake/flaskapp"`

`$env:FLASK_ENV = "development"`

`flask run`

You’ll see output similar to this:

`* Serving Flask app "coursecake/flaskapp"`

`* Environment: development`

`* Debug mode: on`

`* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)`

`* Restarting with stat`

`* Debugger is active!`

`* Debugger PIN: 855-212-761`
