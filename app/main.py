# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1 import lt, gk, users, quantities, law_groups, laws, represents, system_types

app = FastAPI(
    title="FViZ Backend",
    version="0.1.0",
)

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://fviz-frontend-react.vercel.app",
    "https://www.new-fviz.ru",
    "https://new-fviz.ru",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,          # или ["*"] для полного разрешения (не советую для прод)
    allow_credentials=True,         # нужно если используешь cookies/authorization
    allow_methods=["*"],            # GET/POST/PATCH/DELETE...
    allow_headers=["*"],            # Authorization, Content-Type и т.п.
)


app.include_router(lt.router, prefix="/lt", tags=["lt"])
app.include_router(system_types.router, prefix="/system_types", tags=["system_types"])
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(gk.router, prefix="/gk", tags=["gk"])
app.include_router(quantities.router, prefix="/quantities", tags=["quantities"])
app.include_router(law_groups.router, prefix="/law_groups", tags=["law_groups"])
app.include_router(laws.router, prefix="/laws", tags=["laws"])
app.include_router(represents.router, prefix="/represents", tags=["represents"])