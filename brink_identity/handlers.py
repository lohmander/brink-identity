from brink_auth.models import User
from brink.decorators import require_request_model
from brink.exceptions import HTTPNotFound, HTTPBadRequest, HTTPUnauthorized
import jwt

async def handle_auth_user(request):
    data = await request.json()

    try:
        user = await User.authenticate(data["username"], data["password"])
    except KeyError:
        raise HTTPBadRequest(text="Requires both username and password")

    if not user:
        raise HTTPUnauthorized(text="Incorrect username or password")

    token = jwt.encode({"id": user.id}, "secret", algorithm="HS256")
    return 200, {"data": {"token": str(token)}}


async def handle_list_users(request):
    users = await User.all().as_list()
    return 200, { "data": users }


@require_request_model(User)
async def handle_create_user(request, user):
    if not await user.username_available():
        raise HTTPBadRequest(text="username is already taken")

    await user.save()
    return 201, { "data": user }


async def handle_get_user(request):
    id = request.match_info["id"]
    user = await User.get(id)

    if not user:
        raise HTTPNotFound()

    return 200, { "data": user }


@require_request_model(User)
async def handle_update_user(request, user):
    id = request.match_info["id"]
    user.id = id
    await user.save()
    return 200, { "data": user }


async def handle_delete_user(request):
    id = request.match_info["id"]
    User.delete(id)
    return 204, None

