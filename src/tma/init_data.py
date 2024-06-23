from datetime import datetime, timedelta
from src.tma.chat import ChatType
from src.tma.user import User
import json


class InitData:
    def __init__(self, auth_date, hash, chat=None, chat_type=None, chat_instance=None,
                 can_send_after=None, query_id=None, receiver=None, start_param=None, user=None):
        self.auth_date_raw = auth_date
        self.hash = hash
        self.chat = chat
        self.chat_type = ChatType(chat_type) if chat_type else None
        self.chat_instance = chat_instance
        self.can_send_after_raw = can_send_after
        self.query_id = query_id
        self.receiver = receiver
        self.start_param = start_param
        self.user = User(**json.loads(user))

    def auth_date(self):
        return datetime.fromtimestamp(self.auth_date_raw)

    def can_send_after(self):
        if self.can_send_after_raw:
            return self.auth_date() + timedelta(seconds=self.can_send_after_raw)
        return None