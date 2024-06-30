from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "player" (
    "tg_id" BIGSERIAL NOT NULL PRIMARY KEY,
    "cups" INT NOT NULL  DEFAULT 0,
    "foolcoin" INT NOT NULL  DEFAULT 100,
    "toncoin" INT NOT NULL  DEFAULT 0,
    "notcoin" INT NOT NULL  DEFAULT 0,
    "tether" INT NOT NULL  DEFAULT 0,
    "last_claim" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "is_online" BOOL NOT NULL  DEFAULT True,
    "is_free" BOOL NOT NULL  DEFAULT True
);
CREATE TABLE IF NOT EXISTS "game" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "bet" INT NOT NULL,
    "currency" VARCHAR(10) NOT NULL,
    "game_type" VARCHAR(8) NOT NULL,
    "num_players" INT NOT NULL  DEFAULT 0,
    "host_id" BIGINT NOT NULL REFERENCES "player" ("tg_id") ON DELETE CASCADE
);
COMMENT ON COLUMN "game"."currency" IS 'flip_up: flip_up\ntranslated: translated';
COMMENT ON COLUMN "game"."game_type" IS 'toncoin: toncoin\nnotcoin: notcoin\ntether: tether\nfoolcoin: foolcoin';
CREATE TABLE IF NOT EXISTS "gameplayers" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "is_done" BOOL NOT NULL  DEFAULT False,
    "cards" JSONB NOT NULL,
    "player_id" BIGINT NOT NULL REFERENCES "player" ("tg_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "player_player" (
    "player_rel_id" BIGINT NOT NULL REFERENCES "player" ("tg_id") ON DELETE CASCADE,
    "player_id" BIGINT NOT NULL REFERENCES "player" ("tg_id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_player_play_player__0e38b9" ON "player_player" ("player_rel_id", "player_id");
CREATE TABLE IF NOT EXISTS "game_gameplayers" (
    "game_id" INT NOT NULL REFERENCES "game" ("id") ON DELETE CASCADE,
    "gameplayers_id" INT NOT NULL REFERENCES "gameplayers" ("id") ON DELETE CASCADE
);
CREATE UNIQUE INDEX IF NOT EXISTS "uidx_game_gamepl_game_id_6c0525" ON "game_gameplayers" ("game_id", "gameplayers_id");"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
