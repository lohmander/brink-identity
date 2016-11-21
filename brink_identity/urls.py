from brink.urls import GET, POST, PUT, DELETE, WS


urls = [
    POST("/auth", "handlers.handle_auth_user"),
    GET("/users", "handlers.handle_list_users"),
    POST("/users", "handlers.handle_create_user"),
    GET("/users/{id}", "handlers.handle_get_user"),
    PUT("/users/{id}", "handlers.handle_update_user"),
    DELETE("/users/{id}", "handlers.handle_delete_user"),
]
