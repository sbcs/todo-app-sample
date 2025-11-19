# TODO App Sample

This is a simple TODO list app made for our Docker Workshop! We will be using
this app to demonstrate how to containerize applications using Docker.

The frontend is built with HTML/CSS/JavaScript, and the backend is made with
Flask (Python) and Redis (as the *database*).

## Features
- Add new TODO items
- View existing TODO items
- Delete TODO items

## Running in Development
1. `python3 -m venv .venv` to create a virtual environment if not done already.
2. `source .venv/bin/activate` to activate the virtual environment.
3. `pip install -r requirements.txt` to install the required packages.
4. Make sure you have a Redis server running locally on the default port (6379).
If you don't have a Redis server running, you can create one with Docker
Compose: `cd scripts && docker-compose up -d`.
5. `flask run` to start the Flask server.
6. Open your web browser and go to `http://localhost:5000` to access the app.