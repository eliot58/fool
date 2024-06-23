from enum import Enum


class ChatType(str, Enum):
    SENDER = "sender"
    PRIVATE = "private"
    GROUP = "group"
    SUPERGROUP = "supergroup"
    CHANNEL = "channel"

    def known(self):
        return self in {
            ChatType.SENDER,
            ChatType.PRIVATE,
            ChatType.GROUP,
            ChatType.SUPERGROUP,
            ChatType.CHANNEL
        }


class Chat:
    def __init__(self, id, type, title, photo_url=None, username=None):
        self.id = id
        self.type = ChatType(type)
        self.title = title
        self.photo_url = photo_url
        self.username = username