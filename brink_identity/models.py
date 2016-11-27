import hashlib

from brink.models import Model
from brink import fields


class Identity(Model):
    username = fields.Field(required=True)
    password = fields.PasswordField(required=True)
    roles = fields.ListField(fields.CharField(min_length=2))

    async def authenticate(self):
        hash = hashlib.sha256(self.password.encode("utf-8")).hexdigest()
        identities = await Identity \
            .filter({"username": self.username, "password": hash}) \
            .as_list()

        if len(identities) == 1:
            self.wrap(identities[0]._state)
            return True
        else:
            return False

    async def username_available(self):
        return await Identity.filter({"username": self.username}).count() == 0

    def before_save(self):
        self.password = hashlib.sha256(self.password.encode("utf-8")) \
            .hexdigest()
