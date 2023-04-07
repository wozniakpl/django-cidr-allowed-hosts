# Django CIDR Allowed Hosts

A Django middleware that allows you to specify a list of allowed hosts using CIDR notation.

## Installation

Install using pip:
```
pip install django-cidr-allowed-hosts
```

Add the middleware at the top of your `MIDDLEWARE` settings:
```python
MIDDLEWARE = [
    'cidr.middleware.CIDRMiddleware',
    ...
]
```

Add the `CIDR_ALLOWED_HOSTS` setting to your settings:
```python
CIDR_ALLOWED_HOSTS = ["0.0.0.0/0"] # allows any IPv4
```

And that should be it.

## Features

- `ALLOWED_HOSTS` will still work as expected. Since the middleware overrides the `ALLOWED_HOSTS` setting to `"*"`, the value provided originally to `ALLOWED_HOSTS` will be stored in `ORIGINAL_ALLOWED_HOSTS` and used to check if the request should be allowed.
- If `CIDR_ALLOWED_HOSTS` is not set, the middleware will not be used.
- If `ALLOWED_HOSTS` contains `"*"` and `CIDR_ALLOWED_HOSTS` is set, the middleware will raise `MiddlewareNotUsed` exception.
- `CIDR_ALLOWED_HOSTS` must follow the [CIDR notation](https://en.wikipedia.org/wiki/Classless_Inter-Domain_Routing#CIDR_notation).
- Only IPv4 is supported.

## Development

```
python3 -m virtualenv venv
source venv/bin/activate
pip3 install tox
tox
```

## Credits

This project was inspired by [django-allow-cidr](https://github.com/mozmeao/django-allow-cidr)