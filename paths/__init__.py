from . import html#, api

ROUTES = (
    (["GET"], "/", html.home),
    (["GET"], "/login", html.login),
    (["GET"], "/logout", html.logout),
    (["POST"], "/gconnect", html.gconnect),
    (["POST"], "/fbconnect", html.fbconnect),

)
