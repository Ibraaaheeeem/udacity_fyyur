Fyyur - Udacity SQL and Data Modeling Project
-----

## Introduction

Fyyur is a musical venue and artist booking site that facilitates the discovery and bookings of shows between local performing artists and venues. This site lets you list new artists and venues, discover them, and list shows with artists as a venue owner. A starter code was provided and the task was to complete it to full functionality implementing data from database as opposed to hardcoded values within the program

My job was to build out the data models to power the API endpoints for the Fyyur site by connecting to a PostgreSQL database for storing, querying, and creating information about artists and venues on Fyyur.

## Overview

This app was nearly complete. It was only missing real data. While the views and controllers are defined in this application, it was missing models and model interactions to be able to store retrieve, and update data from a database. At the end of this project, I had a fully functioning site that is at least capable of doing the following, if not more, using a PostgreSQL database:

* creating new venues, artists.
* creating new shows.
* searching for venues and artists.
* edit or delete a venue or artist and associated show(s)
* learning more about a specific artist or venue.

## Tech Stack (Dependencies)

### 1. Backend Dependencies
Tech stack used included the following:
 * **virtualenv** as a tool to create isolated Python environments
 * **SQLAlchemy ORM** to be our ORM library of choice
 * **PostgreSQL** as our database of choice
 * **Python3** and **Flask** as our server language and server framework
 * **Flask-Migrate** for creating and running schema migrations
These can be downloaded and installed using `pip` as follows:
```
pip install virtualenv
pip install SQLAlchemy
pip install postgres
pip install Flask
pip install Flask-Migrate
```

### 2. Frontend Dependencies
The app uses **HTML**, **CSS**, and **Javascript** with [Bootstrap 3](https://getbootstrap.com/docs/3.4/customize/) for the website's frontend. 

## 3. Running the app

```cd``` into the project folder
Create a virtual environment using ```python -m venv <name of virtual environment>```
Activate the virtual environment ```source ./path_to_virtual_environment/bin/activate``` - (Linux)
Install requirements using ```pip install -r requirements.txt```
Start the app using ```flask run```
Copy the ip address:port or clink on it to view the app running
