from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from views.devices_online import get_devices_online


app = FastAPI()


@app.get('/')
async def root():
    contents = get_devices_online()
    return HTMLResponse(contents)
