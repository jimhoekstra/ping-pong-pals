# Ping Pong Pals 🏓

This repository contains a Django website that allows users to keep track of game results, 
and updates the Elo rating of players after every game.

## Get Started 💻

To run this application on your machine, follow these steps:

- Clone the application on your computer
- Create a new Python environment (recommended Python version is 3.13)
- Install the dependencies: `uv sync`
- Make sure to set the following environment variables:
  - `DJANGO_DEBUG`
  - `DJANGO_SECRET_KEY`
  - `DJANGO_ALLOWED_HOSTS`
- Run the database migrations with: `uv run manage.py migrate`
- Start the application by running: `uv run manage.py runserver`
- Open a browser and navigate to `http://localhost:8000/`
