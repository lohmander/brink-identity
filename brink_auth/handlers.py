from brink_auth.models import User
from brink.handlers import handle_model
from brink.exceptions import HTTPNotFound, HTTPBadRequest
import jwt

async def handle_auth_user(request):
    user = await User.authenticate("gunnar", "password")
    token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
    return 200, {"data": {"token": str(token)}}


async def handle_list_users(request):
    users = await User.all().without("password").as_list()
    return 200, { "data": users }


@handle_model(User)
async def handle_create_user(request, user):
    if (await User.filter({"username": user.username}).count().run()) > 0:
        raise HTTPBadRequest(text="username is already taken")

    await user.save()
    del user.password
    return 201, { "data": user }


async def handle_get_user(request):
    id = request.match_info["id"]
    user = await User.get(id)

    del user.password

    if not user:
        raise HTTPNotFound()

    return 200, { "data": user }


@handle_model(User)
async def handle_update_user(request, user):
    id = request.match_info["id"]
    user["id"] = id
    await user.save()
    del user.password
    return 200, { "data": user }


async def handle_delete_user(request):
    id = request.match_info["id"]
    User.delete(id)
    return 204, None

