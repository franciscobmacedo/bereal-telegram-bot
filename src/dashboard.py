from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src.db import get_chats
from src.schemas import Chat

app = FastAPI()


templates = Jinja2Templates(directory="src/templates")


@app.get("/chats")
async def chats() -> dict:
    chats = get_chats(only_active=False)
    labels = []
    values = []
    for chat in chats:
        date = chat.created_at.date()
        if date in labels:
            idx = labels.index(date)
            values[idx] += 1
        else:
            labels.append(date)
            values.append(1)
    return {"labels": labels, "values": values}


@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("dashboard.html", {"request": request})
