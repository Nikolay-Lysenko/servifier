# Servifier

## Overview

It is an easy-to-use tool for making web service with API from your own Python functions.

The list of supported and planned features is as follows:
= [x] Concise error messages for end user 
- [] Customizable requests validation
- [] Authentication

## Minimal Example

Suppose that you have a file named `simple_service.py` that looks like this:

```python
from servifier.app_factory import HandleSpec, create_app


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

To be continued.

## Tips on Usage

To be continued.
