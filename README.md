# django-para-search

Django REST API that takes in multiple paragraphs of text as input, stores each paragraph and the words to paragraph mappings on a postgreSQL database.

1.  Fork this repository to your github account.
2.  Clone the forked repository using `git clone https://github.com/tusharrao198/django-para-search.git`
3.  You can have the project running in a virtual environment or otherwise. Virtual environment is a preferred option.

    **Steps to set up a virtual environment for this project**

    1. Create a virtual environment using `python3 -m venv venv`
    2. Activate virtual environment -

        **On Linux** `source venv/bin/activate`

        **On Windows** `venv\Scripts\activate`

    3. Install required modules using `pip3 install -r requirements.txt`.

4.  Store your secrets by adding them at the end of `venv/bin/activate`. They will be set whenever you run the virtual environment.

    **On Linux** `export SECRET_KEY=''`

    **On Windows** `set SECRET_KEY=''`

    To learn how to generate a secret key click [here](https://stackoverflow.com/a/16630719/12350727).
    Remember to restart your virtual environment if you get an error after doing this.

    **OR**

    -   Extract the env.zip file in the project root, provided in the repo.

5.  Change directory using `cd django-para-search`.
6.  Build Docker Image: `sudo docker-compose up --build`

    -   Check your changes before running: `sudo docker-compose run web python manage.py check`.
    -   Make migrations: `sudo docker-compose run web python manage.py makemigrations`.
    -   Migrate Changes: `sudo docker-compose run web python manage.py migrate`.

7.  Run the server on your machine using `python manage.py runserver` and then open [http://0.0.0.0:5055/](http://0.0.0.0:5055/) in your browser.

    -   Superuser is created on running the application for the first time automatically.

8.  Open the Application:-

# Paragraph Search API Documentation

## Authentication Token Generation API

**URL:** `/api-token-auth/`
**Method:** `POST`
**Request Body:**

```
{
  "username": "john",
  "password": "john@123"
}
```

**Response Body:**

```
    {
        "token": <api-auth-token>,
    }
```

## Create User

Creates a new user.

**URL:** `/users/`
**Method:** `POST`
**Request Body:**

```
{
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "password": "john@123",
    "dob": "1990-01-01"
}
```

**Headers:**

```
    Authorization: Token <string>
```

-   Note: Use Token generated via `/api-token-auth/` API of the admin.

**Response Body:**

```
{
    "id": 1,
    "name": "John Doe",
    "email": "john.doe@gmail.com",
    "dob": "1990-01-01",
    "created_at": "2023-04-22T10:00:00Z",
    "modified_at": "2023-04-22T10:00:00Z"
}
```

## Search Paragraphs [GET Request]

Searches for paragraphs containing a given word.

**URL:** `/search/<str:word>/`
**Method:** `GET`
**URL Params:** `word=[string]`
**Response Body:**

```
[
    {
        "id": 1,
        "text": "This is the first paragraph.\n\nIt contains the word search.",
    },
    {
        "id": 2,
        "text": "This is the second paragraph.\n\nIt also contains the word search.",
    }
]
```

## Add Paragraphs [POST Request]

**URL:** `/paragraphs`
**Method:** `POST`
**Request Body:**

```
{
    "paragraphs": "Life is full of challenges\n\nTechnology has revolutionized the way we live, work, and com."
}
```

**Request Body:** `None`
**Status:** `201 Created`
