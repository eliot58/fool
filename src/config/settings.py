import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_URI = f'postgres://{os.environ.get("POSTGRES_USER")}:' \
               f'{os.environ.get("POSTGRES_PASSWORD")}@' \
               f'{os.environ.get("DB_HOST")}:{os.environ.get("DB_PORT")}/' \
               f'{os.environ.get("POSTGRES_DB")}'


SECRET_AUTH = os.environ.get("SECRET_AUTH")

BOT_TOKEN = os.environ.get("BOT_TOKEN")

ADMIN = os.environ.get("ADMIN")

APPS_MODELS = [
    "src.player.models",
    "src.store.models",
    "aerich.models",
]

