[![Build Status](https://travis-ci.org/Nikolay-Lysenko/servifier.svg?branch=master)](https://travis-ci.org/Nikolay-Lysenko/servifier)
[![codecov](https://codecov.io/gh/Nikolay-Lysenko/servifier/branch/master/graph/badge.svg)](https://codecov.io/gh/Nikolay-Lysenko/servifier)
[![Maintainability](https://api.codeclimate.com/v1/badges/b9203957727d2ea2d808/maintainability)](https://codeclimate.com/github/Nikolay-Lysenko/servifier/maintainability)
[![PyPI version](https://badge.fury.io/py/servifier.svg)](https://badge.fury.io/py/servifier)

# Servifier

## Overview

It is an easy-to-use tool for making web service with API from your own Python functions.

The list of the features is as follows:
* fault tolerance,
* customizable requests validation,
* concise error messages for end user,
* authentication.

## Minimal Example

Suppose that you have a file named `simple_service.py` that looks like this:

```python
from servifier import HandleSpec, create_app


def add_numbers(first: int, second: int) -> int:
    """Add two numbers."""
    return first + second


def subtract_numbers(first: int, second: int) -> int:
    """Subtract two numbers."""
    return first - second


handle_spec_for_adding = HandleSpec(add_numbers, '/add')
handle_spec_for_subtraction = HandleSpec(subtract_numbers, '/subtract')

handle_specs = [handle_spec_for_adding, handle_spec_for_subtraction]

app = create_app(handle_specs)
app.run()
```

Run this script. A demo server starts and after that you can send requests to it:

```bash
>>> curl -X POST -H "Content-Type: application/json" -d '{"first": 1, "second": 3}' http://127.0.0.1:5000/add
{"response":4,"status":200}
>>> curl -X POST -H "Content-Type: application/json" -d '{"first": 1, "second": 3}' http://127.0.0.1:5000/subtract
{"response":-2,"status":200}
```

## Installation

A stable version of the package can be collected from PyPI:

```pip install servifier```

## Tips on Usage

#### Deployment on a Production Server

In the above minimal example, the development server provided by `Flask` is used. It is not suitable for production usage.

There are [plenty of ways](http://flask.pocoo.org/docs/1.0/deploying/) to deploy a Flask application on a production server. For example, you can use [Waitress](http://flask.pocoo.org/docs/1.0/tutorial/deploy/#run-with-a-production-server) or uWSGI.

Let us discuss uWSGI a bit more. You can create `uwsgi.ini` config:

```
[uwsgi]
# {Python module}:{Flask app from there}
module = simple_service:app
# If it is true, there is a master process, not only workers.
master = true
# Number of workers.
processes = 4
# Host and port for API, '0.0.0.0' means to use web address.
http = 0.0.0.0:7070
# Directory with code to be imported.
pythonpath = ./venv/lib/python3.6/site-packages/
# If it is not set, logs are printed. If it is set, logs are written to this file.
logto = /tmp/servifier.log
```

To use it, you need to install `uWSGI` Python package:
```
pip install uwsgi
```

To start a production server, delete `app.run()` line from `simple_service.py` (it launches demo server) and run:
```
uwsgi --ini uwsgi.ini
```

It may be enough to have just uWSGI. However, you can also add Nginx in front of uWSGI as a load balancer and a reverse proxy.

#### Input Data Validation

It is possible to configure `servifier` so that requests with invalid data are rejected with a proper error code before your function is called.

The minimal example with a simple service can be modified in the following manner:

```python
from servifier import HandleSpec, create_app
from servifier.validation import IntegerField


def add_numbers(first: int, second: int) -> int:
    """Add two numbers."""
    return first + second


def subtract_numbers(first: int, second: int) -> int:
    """Subtract two numbers."""
    return first - second
    
    
class IntegerPair:
    """A pair of two integers."""
    
    first = IntegerField(required=True)
    second = IntegerField(required=True)
    
    def __init__(self, first: int, second: int):
        """Initialize an instance with parameters validation."""
        self.first = first
        self.second = second


handle_spec_for_adding = HandleSpec(
    add_numbers, '/add', IntegerPair
)
handle_spec_for_subtraction = HandleSpec(
    subtract_numbers, '/subtract', IntegerPair
)

handle_specs = [handle_spec_for_adding, handle_spec_for_subtraction]

app = create_app(handle_specs)
app.run()
```

Behavior of the service is demonstrated below:

```bash
>>> curl -X POST -H "Content-Type: application/json" -d '{"first": "1", "second": 3}' http://127.0.0.1:5000/add
{"error":"Invalid Request: check your JSON","status":422}
```

Comparing to the minimal example, this service returns "Invalid Request" status instead of "Internal Error" status which is harder to debug for end user.

If you need more info about how this example works, read about [Python descriptors](https://www.codevoila.com/post/69/python-descriptors-example).

#### Authentication

It is possible to deny requests that does not include login and token where proper value of token is defined by login and arbitrary salt.

Minimal example with authentication enabled looks like this:

```python
from servifier import HandleSpec, create_app


def add_numbers(first: int, second: int) -> int:
    """Add two numbers."""
    return first + second


def subtract_numbers(first: int, second: int) -> int:
    """Subtract two numbers."""
    return first - second


handle_spec_for_adding = HandleSpec(
    add_numbers, '/add', auth_salt='abcd'
)
handle_spec_for_subtraction = HandleSpec(
    subtract_numbers, '/subtract', auth_salt='1234'
)

handle_specs = [handle_spec_for_adding, handle_spec_for_subtraction]

app = create_app(handle_specs)
app.run()
```

For a particular login, you can generate its token with `servifier.auth.generate_token` function and tell this value to someone sending requests under this login. JSON attachment from a request must include two additional fields ('login' and 'token') besides fields with arguments for a Python function.

```bash
>>> curl -X POST -H "Content-Type: application/json" -d '{"login": "a", "token": "6491cacf01b2e1c6d08a5609d2f570ea57d71ae7f06e0391276d70d935d29aa51888d566751aa36dc5e12e18da693ece36427c167e2a7a67e48aca8928ba3979", "first": 1, "second": 3}' http://127.0.0.1:5000/subtract
{"result":-2,"status":200}
```
