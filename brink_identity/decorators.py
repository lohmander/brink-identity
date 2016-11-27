import jwt
from brink.exceptions import HTTPUnauthorized, HTTPForbidden

from brink_identity.models import Identity


def require_identity(handler):
    """
    Ensures that the user presents a valid authorization token and retrieves
    the corresponding identity from the database and passes it as the second
    argument to the handler. ::

        @require_identity
        async def handler(request, identity):
            return 200, {}
    """
    async def new_handler(request, *args, **kwargs):
        auth_header = request.headers["Authorization"]
        [kind, token] = auth_header.split(" ")

        if kind != "JWT":
            raise HTTPUnauthorized(
                text="Invalid header. Only JWT tokens are allowed.")

        try:
            claims = jwt.decode(token, "secret")
        except:
            raise HTTPUnauthorized(text="Invalid token.")

        identity = await Identity.get(claims["id"])

        return await handler(request, identity, *args, **kwargs)
    return new_handler


def require_identity_role(role):
    """
    Performs the same checks as ``require_identity`` and that the provided
    role is present in the identity role list. ::

        @require_identity_role("admin")
        async def handler(request, identity):
            return 200, {}
    """
    def decorator(handler):
        async def new_handler(request, identity, *args, **kwargs):
            if role not in identity.roles:
                raise HTTPForbidden(
                    text="Insufficient permissions.")

            return await handler(request, identity, *args, **kwargs)
        return require_identity(new_handler)
    return decorator


def require_identity_match(param=None):
    """
    Ensures that the requesting user's id matches that of the provided source.

    The following example shows how to match the requesting user's id against
    the id found in the URL parameters. ::

        @require_identity_match(param="id")
        async def handle_update_user(request, user):
            # ...
            return 200, user
    """
    def decorator(handler):
        async def new_handler(request, identity, *args, **kwargs):
            id = None

            if param is not None:
                id = request.match_info[param]

            if id != identity.id:
                raise HTTPForbidden()

            return await handler(request, identity, *args, **kwargs)
        return require_identity(new_handler)
    return decorator
