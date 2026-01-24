import os
import sys
import argparse
from pathlib import Path

def create_file(path: Path, content: str):
    """Creates a file with the given content."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.strip() + "\n")
    print(f"Created: {path}")

def generate_project(project_name: str, output_dir: str):
    """Generates the FastAPI project structure."""
    
    base_path = Path(output_dir) / project_name
    src_path = base_path / "src" / project_name
    
    # --- Root Files ---
    
    # pyproject.toml
    create_file(base_path / "pyproject.toml", f"""
[project]
name = "{project_name}"
version = "1.0.0"
description = "Production-grade FastAPI Backend"
readme = "README.md"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.115.0",
    "uvicorn[standard]>=0.32.0",
    "sqlalchemy[asyncio]>=2.0.35",
    "asyncpg>=0.30.0",
    "alembic>=1.14.0",
    "pydantic[email]>=2.10.0",
    "pydantic-settings>=2.6.0",
    "python-dotenv>=1.0.1",
    "python-jose[cryptography]>=3.3.0",
    "bcrypt>=4.0.0",
    "python-multipart>=0.0.20",
]

[project.optional-dependencies]
dev = [
    "pytest>=8.3.0",
    "pytest-asyncio>=0.24.0",
    "httpx>=0.28.0",
    "ruff>=0.8.0",
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.ruff]
line-length = 100
target-version = "py311"
""")

    # .env
    create_file(base_path / ".env", f"""
APP_NAME="{project_name.capitalize()} Backend"
ENVIRONMENT=development
DEBUG=True

# Database
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432
DB_NAME={project_name}_db
DATABASE_ECHO=False

# Security
SECRET_KEY=change_this_to_a_secure_random_string_in_production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
""")

    # .gitignore
    create_file(base_path / ".gitignore", """
__pycache__/
*.py[cod]
*$py.class
.env
.venv
venv/
logs/
*.db
.pytest_cache/
.ruff_cache/
""")

    # README.md
    create_file(base_path / "README.md", f"""
# {project_name.capitalize()} Backend

Production-ready FastAPI backend with JWT authentication, SQLAlchemy (Async), and Alembic migrations.

## Setup

1. **Install Dependencies** (using uv or pip):
   ```bash
   pip install .
   # OR if using uv
   uv pip install .
   ```

2. **Environment Variables**:
   Copy `.env` and adjust settings (Database credentials, Secret Key).

3. **Database Setup**:
   Ensure PostgreSQL is running and the database exists.
   ```bash
   # Run migrations
   alembic upgrade head
   
   # Initialize DB and Seed Admin User
   python scripts/init_db.py
   ```

4. **Run Application**:
   ```bash
   uvicorn {project_name}.main:app --reload
   ```

## Default Admin Credentials
- **Username**: Admin
- **Password**: Admin123
""")

    # alembic.ini
    create_file(base_path / "alembic.ini", f"""
[alembic]
script_location = alembic
prepend_sys_path = src
version_path_separator = os

[loggers]
keys = root,sqlalchemy,alembic

[handlers]
keys = console

[formatters]
keys = generic

[logger_root]
level = WARN
handlers = console
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic

[handler_console]
class = StreamHandler
args = (sys.stderr,)
level = NOTSET
formatter = generic

[formatter_generic]
format = %(levelname)-5.5s [%(name)s] %(message)s
datefmt = %H:%M:%S
""")

    # --- Alembic ---
    
    create_file(base_path / "alembic" / "env.py", f"""
import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from {project_name}.core.config import get_settings
from {project_name}.db.base import Base
# Import models here to register them
from {project_name}.modules.users.model import User

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

settings = get_settings()
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={{"paramstyle": "named"}},
    )
    with context.begin_transaction():
        context.run_migrations()

def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {{}})
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
""")
    
    create_file(base_path / "alembic" / "script.py.mako", """
\"\"\"${message}

Revision ID: ${up_revision}
Revises: ${down_revision | comma,n}
Create Date: ${create_date}

\"\"\"
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = ${repr(up_revision)}
down_revision: Union[str, None] = ${repr(down_revision)}
branch_labels: Union[str, Sequence[str], None] = ${repr(branch_labels)}
depends_on: Union[str, Sequence[str], None] = ${repr(depends_on)}


def upgrade() -> None:
    ${upgrades if upgrades else "pass"}


def downgrade() -> None:
    ${downgrades if downgrades else "pass"}
""")

    # --- Source Code ---

    # src/<project>/__init__.py
    create_file(src_path / "__init__.py", "")

    # src/<project>/main.py
    create_file(src_path / "main.py", f"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from {project_name}.core.config import get_settings
from {project_name}.core.logging import setup_logging
from {project_name}.api.v1.router import api_v1_router

setup_logging()
settings = get_settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    yield
    # Shutdown

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Production-ready FastAPI Backend",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_v1_router)

@app.get("/")
async def root():
    return {{"message": "Welcome to {project_name} API", "docs": "/docs"}}
""")

    # --- Core ---
    
    # src/<project>/core/config.py
    create_file(src_path / "core" / "config.py", f"""
from functools import lru_cache
from typing import Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    APP_NAME: str = "FastAPI Project"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True

    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DATABASE_ECHO: bool = False

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    CORS_ORIGINS: list[str] = ["*"]
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"

    @property
    def DATABASE_URL(self) -> str:
        return f"postgresql+asyncpg://{{self.DB_USER}}:{{self.DB_PASSWORD}}@{{self.DB_HOST}}:{{self.DB_PORT}}/{{self.DB_NAME}}"

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            return [x.strip() for x in v.split(",")]
        return v

@lru_cache
def get_settings() -> Settings:
    return Settings()
""")

    # src/<project>/core/security.py
    create_file(src_path / "core" / "security.py", f"""
from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
from jose import jwt
from {project_name}.core.config import get_settings

settings = get_settings()

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

def create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({{"exp": expire, "type": "access"}})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def create_refresh_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode.update({{"exp": expire, "type": "refresh"}})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)

def decode_token(token: str) -> dict[str, Any]:
    return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
""")

    # src/<project>/core/logging.py
    create_file(src_path / "core" / "logging.py", f"""
import logging
import sys
from pathlib import Path
from {project_name}.core.config import get_settings

def setup_logging():
    settings = get_settings()
    Path(settings.LOG_FILE).parent.mkdir(parents=True, exist_ok=True)
    
    logging.basicConfig(
        level=settings.LOG_LEVEL,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(settings.LOG_FILE)
        ]
    )
    
def get_logger(name: str):
    return logging.getLogger(name)
""")

    # src/<project>/core/exceptions.py
    create_file(src_path / "core" / "exceptions.py", """
class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

class NotFoundError(AppException):
    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, 404)

class UnauthorizedError(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, 401)

class ForbiddenError(AppException):
    def __init__(self, message: str = "Forbidden"):
        super().__init__(message, 403)
""")

    # src/<project>/core/dependencies.py
    create_file(src_path / "core" / "dependencies.py", f"""
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from {project_name}.db.session import async_session_maker

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        try:
            yield session
        finally:
            await session.close()
""")

    # --- DB ---
    
    # src/<project>/db/base.py
    create_file(src_path / "db" / "base.py", """
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass
""")

    # src/<project>/db/session.py
    create_file(src_path / "db" / "session.py", f"""
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine, AsyncSession
from {project_name}.core.config import get_settings

settings = get_settings()

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    pool_pre_ping=True
)

async_session_maker = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)
""")

    # --- Modules: Auth ---
    
    # src/<project>/modules/auth/router.py
    create_file(src_path / "modules" / "auth" / "router.py", f"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from {project_name}.core.dependencies import get_db
from {project_name}.modules.auth.schema import LoginRequest, TokenResponse
from {project_name}.modules.auth.service import AuthService

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=TokenResponse)
async def login(
    data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    service = AuthService(db)
    return await service.login(data.username, data.password)
""")

    # src/<project>/modules/auth/schema.py
    create_file(src_path / "modules" / "auth" / "schema.py", """
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
""")

    # src/<project>/modules/auth/service.py
    create_file(src_path / "modules" / "auth" / "service.py", f"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from {project_name}.modules.users.model import User
from {project_name}.core.security import verify_password, create_access_token, create_refresh_token
from {project_name}.core.exceptions import UnauthorizedError

class AuthService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def login(self, username: str, password: str):
        result = await self.db.execute(select(User).where(User.username == username))
        user = result.scalar_one_or_none()

        if not user or not verify_password(password, user.hashed_password):
            raise UnauthorizedError("Invalid credentials")
        
        if not user.is_active:
            raise UnauthorizedError("User inactive")

        token_data = {{"sub": str(user.id), "username": user.username, "role": user.role}}
        return {{
            "access_token": create_access_token(token_data),
            "refresh_token": create_refresh_token(token_data)
        }}
""")

    # src/<project>/modules/auth/dependencies.py
    create_file(src_path / "modules" / "auth" / "dependencies.py", f"""
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from {project_name}.core.dependencies import get_db
from {project_name}.core.security import decode_token
from {project_name}.modules.users.model import User
from sqlalchemy import select

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    try:
        payload = decode_token(credentials.credentials)
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token")
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

    result = await db.execute(select(User).where(User.id == int(user_id)))
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=401, detail="User not found")
    
    return user

async def get_admin_user(user: User = Depends(get_current_user)) -> User:
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="Admin privileges required")
    return user
""")

    # --- Modules: Users ---
    
    # src/<project>/modules/users/model.py
    create_file(src_path / "modules" / "users" / "model.py", f"""
from sqlalchemy import Integer, String, Boolean, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime
from {project_name}.db.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(100), unique=True, nullable=True)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), default="user")
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
""")

    # src/<project>/modules/users/router.py
    create_file(src_path / "modules" / "users" / "router.py", f"""
from fastapi import APIRouter, Depends
from {project_name}.modules.auth.dependencies import get_current_user, get_admin_user
from {project_name}.modules.users.model import User

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {{"id": user.id, "username": user.username, "role": user.role}}

@router.get("/admin-only")
async def admin_route(user: User = Depends(get_admin_user)):
    return {{"message": "Hello Admin", "user": user.username}}
""")

    # --- API Router ---
    
    # src/<project>/api/v1/router.py
    create_file(src_path / "api" / "v1" / "router.py", f"""
from fastapi import APIRouter
from {project_name}.modules.auth.router import router as auth_router
from {project_name}.modules.users.router import router as users_router

api_v1_router = APIRouter(prefix="/api/v1")
api_v1_router.include_router(auth_router)
api_v1_router.include_router(users_router)
""")

    # --- Scripts ---
    
    # scripts/init_db.py
    create_file(base_path / "scripts" / "init_db.py", f"""
import asyncio
import sys
from pathlib import Path
# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from sqlalchemy import select
from {project_name}.db.session import engine, async_session_maker
from {project_name}.db.base import Base
from {project_name}.modules.users.model import User
from {project_name}.core.security import hash_password

async def init_db():
    async with engine.begin() as conn:
        # For dev: drop and recreate
        # await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    async with async_session_maker() as session:
        # Check for Admin
        result = await session.execute(select(User).where(User.username == "Admin"))
        admin = result.scalar_one_or_none()
        
        if not admin:
            print("Creating default Admin user...")
            admin_user = User(
                username="Admin",
                hashed_password=hash_password("Admin123"),
                role="admin",
                is_active=True
            )
            session.add(admin_user)
            await session.commit()
            print("Admin user created: Admin / Admin123")
        else:
            print("Admin user already exists.")

if __name__ == "__main__":
    asyncio.run(init_db())
""")

    print(f"\\nSuccessfully generated project '{project_name}' at {base_path}")
    print("Follow the instructions in README.md to get started.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a FastAPI backend project.")
    parser.add_argument("name", nargs="?", default="fastapi_backend", help="Project name")
    parser.add_argument("--output", default=".", help="Output directory")
    
    args = parser.parse_args()
    generate_project(args.name, args.output)
