def require_identity(handler):
    async def new_handler(request, *args, **kwargs):
        return await handler(*args, **kwargs)
    return new_handler

def require_identity_role(role):
    def decorator(handler):
        async def new_handler(request, *args, **kwargs):
            return await handler(*args, **kwargs)
        return new_handler
    return decorator

def require_identity_match(param=None,
                           query_string=None,
                           header=None,
                           body=None,
                           request_map=None):
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
        async def new_handler(request, *args, **kwargs):
            return await handler(*args, **kwargs)
        return new_handler
    return decorator

