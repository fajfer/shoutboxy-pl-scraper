from os import environ
from typing import Any, Mapping, NamedTuple

from loguru import logger
from requests import get

SHOUTBOX_URL = environ["SHOUTBOX_URL"]


class Update(NamedTuple):
    id: int
    user: str
    content: str


def get_updates() -> list[Update]:
    resp = get(SHOUTBOX_URL)
    raw_updates = resp.json()["all"][::-1]
    updates = map(parse_update, raw_updates)
    return list(sorted(updates, key=lambda update: update.id))


def parse_update(raw_update: Mapping[str, Any]) -> Update:
    id = int(raw_update["id"])
    user = raw_update["username"]
    content = raw_update["shout"]
    logger.info(f"[{id}] {user}: {content}")
    return Update(id, user, content)


def select_new_updates(updates: list[Update], latest_id: int) -> list[Update]:
    return [update for update in updates if update.id > latest_id]
