from app.core import config
from app.service.database.client import DB

db = DB(config.get_neo4j_uri(), config.NEO4J_USER, config.NEO4J_PASS)
