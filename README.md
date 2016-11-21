# Authentication app for Brink

## Installation

```
$ pip3 install brink_identity
```

and add it to your installed apps

```python
INSTALLED_APPS = [
    "brink_identity",
    ...
]
```

## Overview

The app will setup the following API urls

### POST: /auth

Authenticate as a user. Returns a JWT token.

### GET: /users

Fetches a list of users.

### POST: /users

Creates a new user.

### GET: /users/{id}

Fetch a specific user.

### PUT: /users/{id}

Update a user.

### DELETE: /users/{id}

Deletes a user.
