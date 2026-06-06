from fastapi import FastAPI
# from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api.search import router as search_router
from .api.contacts import router as contacts_router

app = FastAPI(
    title=
    "AI Contact Intelligence"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    search_router
)

app.include_router(
    contacts_router
)


@app.get("/")
async def health():

    return {
        "status":
        "healthy"
    }