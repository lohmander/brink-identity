import hashlib
import brink.models as models


class User(models.Model):

    schema = {
        "username": {"type": "string", "required": True},
        "password": {"type": "string", "required": True, "minlength": 6}
    }

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

    def before_save(self):
        self["password"] = hashlib.sha256(self["password"].encode("utf-8")) \
            .hexdigest()

