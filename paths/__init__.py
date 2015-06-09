from . import html#, api

ROUTES = (
    (["GET"],         "/",    html.home),
    (["GET", "POST"], "/",    html.home),
)
