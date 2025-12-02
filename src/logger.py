import logging

logging.basicConfig(
    level=logging.INFO,  # Set the default log level to INFO
    format="%(asctime)s + %(name)s + %(levelname)s + %(message)s",
)

logger = logging.getLogger(__name__)
