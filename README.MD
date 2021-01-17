# Network time tracker
This is tool for system administrators for tracking how long devices have been online. 

It has two parts: backend service, which track online time and web-interface application, which runs web-server at 
http://localhost:8000 and allows you to watch statistics of online time for each device.

# How to run the app

## First of all
You need to get dependencies with poetry
```bash
poetry install
```

## How to run backend
And then run backend.py with python
```bash
python backend.py
```

## How to run web-interface
To run web-app you need to start uvicorn web-server like this
```bash
uvicorn web_app:main --workers 1
```
