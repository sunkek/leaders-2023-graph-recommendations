from app.core import config
from app.service.database import db
from app.service.importer.service import import_all
from app.service.rest import api


if __name__ == "__main__":
    if config.NEEDS_IMPORT:
        import_all()

    api.run(host=config.API_HOST, port=config.API_PORT, log_level=config.LOG_LEVEL)
    db.close()
