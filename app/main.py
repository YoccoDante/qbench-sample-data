import logging
import logging.config

from app import create_app
from app.api import api
from app.config import Config


log = logging.getLogger(__name__)

app = create_app()

# Get LOG_LEVEL from app.config after app creation
log_level = app.config.get("LOG_LEVEL", "INFO").upper()  # Default to INFO
level = logging.getLevelName(log_level)

logging.basicConfig(level=level, format="%(asctime)s %(levelname)s - %(message)s - %(name)s")


# Initialize the logging
log.info(f"Starting {Config.ENV} server...")

# Disable Swagger UI in production
if Config.ENV == "production":
    api.doc = False

api.init_app(app)

if __name__ == "__main__":
    app.run()
