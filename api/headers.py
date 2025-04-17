from .shared.iterable import Iterable


class Headers(Iterable):
    user_agent = "User-Agent"
    authorization = "Authorization"
    www_authenticate = "WWW-Authenticate"
    content_type = "Content-Type"
    last_modified = "Last-Modified"
