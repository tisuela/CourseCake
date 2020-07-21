from ...config import Config


def verifyAdminToken(token: str) -> bool:
    return token == Config.ADMIN_TOKEN
