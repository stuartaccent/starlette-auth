import sqlalchemy as sa
from sqlalchemy_utils import EmailType

from starlette_core.database import metadata

user = sa.Table(
    "user",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("email", EmailType, nullable=False, index=True, unique=True),
    sa.Column("password", sa.String(255)),
    sa.Column("first_name", sa.String(120)),
    sa.Column("last_name", sa.String(120)),
    sa.Column("is_active", sa.Boolean, nullable=False, default=True),
    sa.Column("last_login", sa.DateTime, nullable=True),
)

scope = sa.Table(
    "scope",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("code", sa.String(50), nullable=False, unique=True),
    sa.Column("description", sa.Text),
)

user_scope = sa.Table(
    "user_scope",
    metadata,
    sa.Column("user_id", sa.Integer, sa.ForeignKey("user.id"), primary_key=True),
    sa.Column("scope_id", sa.Integer, sa.ForeignKey("scope.id"), primary_key=True),
)
