import os

import uvicorn
import httpx

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")


async def bot_send_message(text: str) -> None:
    async with httpx.AsyncClient() as client:
        bot_token = os.getenv("BOT_TOKEN")
        chat_id = os.getenv("HOOKAHMAN_ID")
        url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
        params = {
            "chat_id": chat_id,
            "text": text,
        }
        await client.get(url, params=params)


@app.get("/table/{id}", response_class=HTMLResponse)
async def table(request: Request, id: str):
    return templates.TemplateResponse("table.html", {"request": request, "id": id})


@app.get("/order/{id}", response_class=HTMLResponse)
async def order(request: Request, id: str):
    text = f"Столик {id} хоче зробити замевлення."
    response = await bot_send_message(text)
    print(response)
    return templates.TemplateResponse("order.html", {"request": request, "id": id})


@app.get("/pay/{id}", response_class=HTMLResponse)
async def pay(request: Request, id: str, payment_method: str | None = None):
    payment_method = "картою" if payment_method == "card" else "готівкою"
    text = f"Столик {id} хоче розрахуватись {payment_method}"
    response = await bot_send_message(text)
    print(response)
    return templates.TemplateResponse(
        "payment.html", {"request": request, "id": id, "payment_method": payment_method}
    )


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
