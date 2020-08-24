import secrets

from ....config import Config


def verifyAdminToken(token: str) -> bool:
    return secrets.compare_digest(token, Config.ADMIN_TOKEN)
