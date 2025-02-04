from typing import Annotated

from fastapi import FastAPI, Depends
from starlette.responses import RedirectResponse

from auth365.providers.google import GoogleOAuth
from auth365.schemas import OAuth2Callback, OpenID
from examples.config import settings

app = FastAPI()

oauth = GoogleOAuth(
    settings.google_client_id,
    settings.google_client_secret,
    "http://localhost:8000/callback",
)


@app.get("/login")
async def login() -> RedirectResponse:
    async with oauth:
        url = await oauth.get_authorization_url()
        return RedirectResponse(url=url)


@app.get("/callback")
async def oauth_callback(callback: Annotated[OAuth2Callback, Depends()]) -> OpenID:
    async with oauth:
        await oauth.authorize(callback)
        return await oauth.userinfo()
