from starlette.authentication import (
    AuthCredentials,
    AuthenticationBackend,
    BaseUser,
    UnauthenticatedUser,
)
from starlette.requests import HTTPConnection

from starlette_auth.utils import db


class ModelUser(BaseUser):
    def __init__(self, user) -> None:
        self.user = user

    @property
    def is_authenticated(self) -> bool:
        return self.user["is_active"]

    @property
    def display_name(self) -> str:
        return self.user["first_name"] + " " + self.user["last_name"]


class ModelAuthBackend(AuthenticationBackend):
    async def get_user(self, conn: HTTPConnection):
        user_id = conn.session.get("user")
        if user_id:
            try:
                return await db.get_user_by_id(user_id)
            except:
                conn.session.pop("user")

    async def authenticate(self, conn: HTTPConnection):
        user = await self.get_user(conn)
        if user and user["is_active"]:
            used = await db.get_user_scopes(user["id"])
            return (
                AuthCredentials(["authenticated"] + sorted([s["code"] for s in used])),
                ModelUser(user),
            )
        return AuthCredentials(["unauthenticated"]), UnauthenticatedUser()
