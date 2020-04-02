from starlette_auth.tables import scope, user_scope, user
from starlette_core.database import database


async def get_user_by_email(email: str):
    query = user.select().where(user.c.email == email)
    return await database.fetch_one(query=query)


async def get_user_by_id(id: int):
    query = user.select().where(user.c.id == id)
    return await database.fetch_one(query=query)


async def get_user_scopes(id: int):
    join = scope.join(user_scope)
    query = scope.select().select_from(join).where(user_scope.c.user_id == id)
    return await database.fetch_all(query=query)


async def update_user(id: int, **values):
    query = user.update().values(**values).where(user.c.id == id)
    return await database.execute(query=query)
