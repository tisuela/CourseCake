from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(
    key_func = get_remote_address,
    default_limits = ["20/second; 60/minute; 600/hour"]
)
