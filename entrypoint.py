import traceback
from logging import getLogger
from time import sleep

from pycontainerutils.db.BaseDB_Adapter import BaseDBAdapter
from pycontainerutils.db.DB_Adapter import DBAdapter
from pycontainerutils.logger.setting_logger import Log_settings

from Controller.logger_config import main_loggers_config
from settings import CONTAINTER_NAME, DATABASES, DB_NICKNAME, IS_MAIN_RUNNING, MAIN_INTERVAL

logger = getLogger(__name__)

if __name__ == '__main__':
    print(f"{CONTAINTER_NAME}: logger settings")

    # 로그 설정
    Log_settings.logger_settings(
        logger_config=main_loggers_config,
        container_name=CONTAINTER_NAME,
        db_info=DATABASES[DB_NICKNAME]
    )
    # db 설정
    BaseDBAdapter.init_settings(
        databases=DATABASES,
        default_db_name=DB_NICKNAME,
        # is_echo_sql="debug",
        is_echo_sql=False,
    )
    logger.info(f"{CONTAINTER_NAME}:  run main")
    # db 에 연결 확인 저장
    db = DBAdapter(name=f"main db")
    update_sql = f"UPDATE app_model_container " \
                 f"SET state = '컨테이너 생성 완료, 메인코드 실행' " \
                 f"WHERE name = '{CONTAINTER_NAME}'"
    db.execute_sql(update_sql)
    try:
        from Controller.manager_engine import EngineManager
        # main run
        engine_manager = EngineManager(container=CONTAINTER_NAME)
        engine_list = engine_manager.load_engine()
        # 스케줄러 실행
        for engine in engine_list:
            engine.scheduler_run()
        # 그냥 main 실행
        import main
        pass
    except Exception as e:

        logger.error(f"{CONTAINTER_NAME}: main running error\n"
                     f"{traceback.format_exc()}")

    # main 동작 유지
    update_sql = f"UPDATE app_model_container " \
                 f"SET state = '동작 완료 main 유지' " \
                 f"WHERE name = '{CONTAINTER_NAME}'"
    db.execute_sql(update_sql)
    while IS_MAIN_RUNNING:
        logger.debug(f"{CONTAINTER_NAME}: running main process")
        sleep(MAIN_INTERVAL)

    logger.info(f"{CONTAINTER_NAME}: end main")
