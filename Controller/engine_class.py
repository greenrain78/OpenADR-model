from datetime import datetime
from logging import getLogger

from pycontainerutils.db.DB_Adapter import DBAdapter
from pycontainerutils.schedule.schedule_manager import MainScheduler

from settings import CONTAINTER_NAME

logger = getLogger(__name__)


class BaseEngine:
    db = DBAdapter(name="BaseEngine")
    table_name = f"app_model_engine"

    def __init__(self, name, module_name, container):
        self.scheduler = MainScheduler(name="CollectBaseMachine")
        self.container = container
        self.name = name
        self.module_name = module_name
        self.cycle = None
        self.reload_engine()

    def container_run(self):
        """ 기본 스케줄러 등록 -컨테이너에서 실행
        """
        print("???")
        logger.info("오버라이딩 안함")
        pass

    def container_run_manager(self):
        """ 기본 스케줄러 등록 -컨테이너에서 실행
        """
        self.container_run()
        update_sql = f"UPDATE {self.table_name} " \
                     f"SET status = '주기적 실행 완료 - {datetime.now()}' " \
                     f"WHERE name = '{self.name}' " \
                     f"AND container_name = '{self.container}'"
        db.execute_sql(update_sql)
        pass

    def reload_engine(self):
        # db 조회
        select_sql = f"SELECT cycle " \
                     f"FROM {self.table_name} " \
                     f"WHERE container_name = '{self.container}' " \
                     f"AND name = '{self.name}' " \
                     f"AND module_name = '{self.module_name}' "
        time_list = self.db.fetch_data_by_sql(select_sql)[0][0]
        # 시간 갱신
        time_dict = {}
        for time_args in time_list:
            if len(time_args) == 2:
                # if second 기타 등등 인지 확인
                time_dict[time_args[0]] = int(time_args[1])
            else:
                raise SyntaxError(f"time 인자를 잘못 입력하셨습니다.")

        self.cycle = time_dict
        # 작업 등록
        try:
            self.scheduler.create_job(
                self.container_run, trigger="interval",
                **self.cycle)
            logger.info(f"{self.name}: 스케줄러 등록 성공\n"
                        f"{self.cycle}")
        except Exception as e:
            raise SyntaxError(f"스케줄 등록에 실패\n"
                              f"cycle: {self.cycle}\n"
                              f"e: {e}")
        pass

    def scheduler_run(self):
        self.scheduler.run()
        logger.info(f"{self.name}: 스케줄러 실행\n"
                    f"{self.cycle}")


class Engine(BaseEngine):
    pass
