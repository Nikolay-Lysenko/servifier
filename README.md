# Servifier

## Overview

It is an easy-to-use tool for making web service with API from your own Python functions.

The list of supported and planned features is as follows:
- [x] Fault tolerance
- [x] Customizable requests validation
- [x] Concise error messages for end user 
- [x] Authentication

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

#### Input Data Validation

It is possible to configure `servifier` so that requests with invalid data are rejected with a proper error code before your function is called.

Above example with a simple service can be modified in the following manner:

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

It is possible to deny requests that does not include login and token where proper value of token is defined by login and hash salt.

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
