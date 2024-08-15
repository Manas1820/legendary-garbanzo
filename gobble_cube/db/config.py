from typing import List

from gobble_cube.settings import settings

MODELS_MODULES: List[str] = [
    "gobble_cube.db.models",
]

TORTOISE_CONFIG = {
    "connections": {
        "default": str(settings.db_url),
    },
    "apps": {
        "models": {
            "models": MODELS_MODULES,
            "default_connection": "default",
        },
    },
}
