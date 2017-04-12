# Campolutions - Andela Campus Idea box
This is a full stack flask application that adds users and allows them to add their ideas

The application is hosted on Heroku. You can view the Idea Box application at [campolutions.herokuapp.com](https://campolutions.herokuapp.com/)

## Getting Started
These instructions should help you run the code on your machine.

### Prerequisites
The code is written in Python3

### Installing

start by cloning the repository from GitHub:

for https use
```
$ git clone https://github.com/Sharonsyra/bc-16-Campolutions-idea-box.git
```

for ssh use 
```
git@github.com:Sharonsyra/bc-16-Campolutions-idea-box.git
```

Change Directory into the project folder
```
$ cd bc-16-Campolutions-idea-box
```

Install the application's dependencies from `requirements.txt`
```
$ pip install -r requirements.txt
```

### Running the program

Run the database model file to create your database. In this case it will create userideas.db in your working directory

```
$python database_setup.py
```
 
To browse your database, download the [sqlite browser](http://sqlitebrowser.org/)

Run the Flask application by typing:
```
$ python project.py
```

### Major Libraries Used
- [Flask](http://flask.pocoo.org/) - A microframework for Python based on Werkzeug, Jinja 2 and good intentions.
- [Markdown language](http://flask.pocoo.org/snippets/19/) - This is a Python implementation of John Gruber’s Markdown. It is almost completely compliant with the reference implementation, though there are a few known issues. See Features for information on what exactly is supported and what is not. Additional features are supported by the Available Extensions.s
- [SQLAlchemy](https://www.sqlalchemy.org/) - SQLAlchemy is the Python SQL toolkit and Object Relational Mapper that gives application developers the full power and flexibility of SQL.
- [Werkzeug](http://werkzeug.pocoo.org/) - Werkzeug is a WSGI utility library for Python. It's widely used and BSD licensed.


## Resources Used
- Udacity Full Stack Foundations by instructor Lorenzo Brown [Full Stack Foundations](https://www.udacity.com/course/full-stack-foundations--ud088)
- Scotch.io Tutorial - [Getting Started with Flask, a Python Framework](https://scotch.io/tutorials/getting-started-with-flask-a-python-microframework)
- flask.pocoo.org documentation [Flask web development, one drop at a time](http://flask.pocoo.org/docs/0.12/)

