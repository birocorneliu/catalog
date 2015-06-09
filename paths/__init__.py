from . import html#, api

ROUTES = (
    (["GET"], "/", html.home),
    (["GET"], "/login", html.login),
    (["POST"], "/gconnect", html.gconnect),

)
