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

## How to use backend
To run backend.py with python use command
```bash
python backend.py
```
Data is stored at file `data.piclke` which is stored in directory where you start this app. After application restart new 
data will be appended to old data, so, if you want to start over writing statistics - just delete, rename or move this 
file somewhere.

## How to run web-interface
To run web-app you need to start uvicorn web-server like this
```bash
uvicorn web_app:main --workers 1
```
