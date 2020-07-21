from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

# enforces rate limits for ALL routes
limiter = Limiter(
    key_func = get_remote_address,
    default_limits = ["1/second; 20/minute"])
