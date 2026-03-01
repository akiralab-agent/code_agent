import firebase_admin
from firebase_admin import credentials, db

from src.infrastructure.config.settings import get_settings

_app: firebase_admin.App | None = None


def get_firebase_app() -> firebase_admin.App:
    global _app
    if _app is not None:
        return _app

    settings = get_settings()
    cred = credentials.Certificate(settings.FIREBASE_SERVICE_ACCOUNT_KEY_PATH)
    _app = firebase_admin.initialize_app(
        cred,
        {"databaseURL": settings.FIREBASE_DATABASE_URL},
    )
    return _app


def get_db_reference(path: str) -> db.Reference:
    get_firebase_app()
    return db.reference(path)
