from brink.urls import GET, POST, PUT, DELETE, WS


urls = [
    POST("/auth", "handlers.handle_auth_identity"),
    GET("/identities", "handlers.handle_list_identities"),
    POST("/identities", "handlers.handle_create_identity"),
    GET("/identities/{id}", "handlers.handle_get_identity"),
    PUT("/identities/{id}", "handlers.handle_update_identity"),
    DELETE("/identities/{id}", "handlers.handle_delete_identity"),
]
