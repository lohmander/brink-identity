from brink.models import Model
from brink import fields
import hashlib


class User(Model):
    username = fields.Field(required=True)
    password = fields.PasswordField()

    @staticmethod
    async def authenticate(username, password):
        hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
        users = await User \
            .filter({"username": username, "password": hash}) \
            .as_list()

        if len(users) == 1:
            return users[0]
        else:
            return None

    async def username_available(self):
        return await User.filter({"username": self.username}).count().run() == 0

    def before_save(self):
        self.password = hashlib.sha256(self.password.encode("utf-8")) \
            .hexdigest()

