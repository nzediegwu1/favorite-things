# Favourite-things

[![CircleCI](https://circleci.com/gh/nzediegwu1/favorite-things.svg?style=svg)](https://circleci.com/gh/nzediegwu1/favorite-things)  [![Maintainability](https://api.codeclimate.com/v1/badges/95b0d3c5a1019ec14339/maintainability)](https://codeclimate.com/github/nzediegwu1/favorite-things/maintainability) [![Coverage Status](https://coveralls.io/repos/github/nzediegwu1/favorite-things/badge.svg?branch=master)](https://coveralls.io/github/nzediegwu1/favorite-things?branch=master)

A full stack web an application that allows the user to track their favorite things.

- Frontend Repo: [Click here](https://github.com/nzediegwu1/favorite-things-ui)

## Table of Contents

    1. Features
    2. Technologies
    3. Entity relationship diagram
    4. Installation and Setup
    5. Suggested improvement
    6. Documentation
    7. Deployment
    8. How To Contribute

## Features

#### Users can perform the following actions with this application

      - Create a Category for saving favourite things
      - Edit a category
      - Delete a category (Soft-delete)
      - View a list of categories and the count of favourites under each
      - Add favourite things under a category
      - Add metadata to a favourite thing
      - Remove metadata from a favourite thing
      - Edit an existing Favourite thing
      - Delete a favourite thing (Soft-delete)
      - View list of favourite things under a category
      - View list of metadata under a Favourite thing
      - View Audit-logs for mutations (create, update, delete) to a Favourite thing
      - Veiw Audit-logs  for mutations (create, update, delete) to a Category
      - Search for Favourite things under a selected Category

## Technologies

    1. Python 3.7
    2. Django and Django REST Framework
    3. Postgres database
    4. pylint, pep8 and yapf for linting
    5. coverage and coveralls for reporting test coverage
    5. Postman for testing API endpoints and documentation

## Entity relationship diagram

![](/entity-diagram.png)

## Installation and Setup

### Development

    1. Install Python 3.7, pipenv and Postgres SQL
    2. Clone this repo: "git clone https://github.com/nzediegwu1/favorite-things.git"
    3. Create virtual environment: `pipenv shell`
    4. Run `pipenv install` to install dependencies
    5. Create a Postgresql database
    6. Create a ".env" file and enter database credentials using sample file: `.env.sample` in the root directory.
    7. Run migrations: `python manage.py migrate`
    8. Start the application: `python manage.py runserver`
    9. Run tests: `python manage.py test`

### Finally

    Go to http://localhost:7000 on your browser to view app

## Documentation

- The API was documented using postman:
  [Online Documentation](https://documenter.getpostman.com/view/4912237/SVYow1PC?version=latest)

## Deployment

This is done using AWS Fargate, with the following steps:
1. Build docker image:
 `docker build -t favourite-things --build-arg DB_USER=<DB_USER> --build-arg DB_PASS=<DB_PASS> --build-arg POSTGRES_DB=<POSTGRES_DB> --build-arg DB_HOST=<DB_HOST> .`
2. Run docker image: `docker run -p 7000:7000 -t favourite-things:latest`
3. Go to `http://127.0.0.1:7000/categories` on your machine to confirm that docker app is running
4. Create AWS container registry: `aws ecr create-repository --repository-name favourite-things --region us-east-1
5. Push docker image to your new AWS container registry
6. Create your fargate application in AWS dashboard
7. View running application using `Public IP` generated in your AWS dashboard

## Suggested improvement

    - Implement recycle bin for deleted favourites/categories
    - Implement functionality to restore deleted favourites/categories from recycle bin
    - Implement pagination when retrieving favorites
    - Integrate elastic search in backend and refactor implemented search functionality correspondingly
    - Implement logging for keeping track of, and easier debugging of production issues when they occur

## How to Contribute

To contribute to the project, follow the instructions below

1.  **Fork** the repo on GitHub
2.  **Clone** the project to your own machine
3.  **Commit** changes to your own branch
4.  **Push** your work back up to your fork
5.  Submit a **Pull request** so that I can review your changes

**NOTE**: Be sure to merge the latest from "upstream" before making a pull request!

## Licence

- This project is licensed under the [MIT License](https://github.com/nzediegwu1/crypto-currency-tracker/blob/master/LICENSE)
- Copyright © 2019 Anaeze Nsoffor
