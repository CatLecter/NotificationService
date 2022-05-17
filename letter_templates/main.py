from typing import List

from fastapi import BackgroundTasks, FastAPI, Request
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema
from pydantic import BaseModel, EmailStr
from starlette.responses import JSONResponse

from letter_templates.interface import create_html

app = FastAPI()


class EmailSchema(BaseModel):
    email: List[EmailStr]


@app.post("/email")
async def send_email(
        background_tasks: BackgroundTasks,
        email: EmailSchema,
        request: Request,
) -> JSONResponse:
    html = create_html()
    message = MessageSchema(
        subject="Fastapi-Mail module",
        recipients=email.dict().get("email"),
        body=str(html),
        subtype="html",
    )
    fm: FastMail = request.app.state.fm
    background_tasks.add_task(fm.send_message, message)
    return JSONResponse({"success": True})


@app.on_event("startup")
async def startup() -> None:
    config = ConnectionConfig()
    app.state.fm = FastMail(config)
