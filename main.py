from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import DATABASE_URI, APPS_MODELS
from src.player.router import router as player_router
from src.game.router import router as game_router
from tortoise.contrib.fastapi import register_tortoise

app = FastAPI(
    title="Fool"
)

app.include_router(player_router)

app.include_router(game_router)

origins = ['*']
    
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PATCH", "PUT"],
    allow_headers=["Content-Type", "Set-Cookie", "Access-Control-Allow-Headers", "Access-Control-Allow-Origin",
                   "Authorization"],
)


register_tortoise(
    app,
    db_url=DATABASE_URI,
    modules={"models": APPS_MODELS},
    generate_schemas=True,
    add_exception_handlers=True,
)