class User:
    def __init__(self, id, first_name, added_to_attachment_menu=False, allows_write_to_pm=False,
                 is_bot=False, is_premium=False, last_name=None, username=None, language_code=None, photo_url=None):
        self.id = id
        self.first_name = first_name
        self.added_to_attachment_menu = added_to_attachment_menu
        self.allows_write_to_pm = allows_write_to_pm
        self.is_bot = is_bot
        self.is_premium = is_premium
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.photo_url = photo_url