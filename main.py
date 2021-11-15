from Controller.logger_config import main_loggers_config
from src.Logger.setting_logger import log_settings
from logging import getLogger

logger = getLogger(__name__)

if __name__ == '__main__':

    print("openadr model")
    log_settings.logger_settings(logger_config=main_loggers_config)
    print("running")
    logger.debug("running")
    logger.info("running")
    logger.error("running")
