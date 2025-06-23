import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
from pydantic import BaseModel

from moderation import detect_banned_words
from worker import amqp_worker


@asynccontextmanager
async def lifespan(app: FastAPI):
    asyncio.create_task(amqp_worker())
    yield

app = FastAPI(
    title="Bazario Moderation",
    version="1.0.0",
    lifespan=lifespan,
)
