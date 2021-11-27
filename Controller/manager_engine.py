from importlib import import_module
from logging import getLogger

from pycontainerutils.db.DB_Adapter import DBAdapter

from Controller.db_sql import update_engine_info

logger = getLogger(__name__)


class EngineManager:
    table_name = f"app_model_engine"
    db = DBAdapter(name="EngineManager")

    def __init__(self, container):
        self.container = container

    def load_engine(self):
        # db 조회
        select_sql = f"SELECT name, module_name, cycle " \
                     f"FROM {self.table_name} " \
                     f"WHERE container_name = '{self.container}'"
        engine_list = self.db.fetch_data_by_sql(select_sql)
        # 객체 import
        obj_list = self.create_engine(engine_list=engine_list)
        return obj_list

    def create_engine(self, engine_list):
        # 객체 생성
        obj_list = []
        for engine in engine_list:
            try:
                # 클래스 import
                tmp_class = import_class(module_name=f"model.{engine[1]}", class_name=engine[0])
                obj_list.append(
                    tmp_class(
                        name=engine[0],
                        module_name=engine[1],
                        container=self.container,
                    )
                )
                # 상태 업데이트
                update_sql = update_engine_info(
                    table_name=self.table_name,
                    where_dict={
                        "container_name": self.container,
                        "name": engine[0],
                        "module_name": engine[1],
                    },
                    set_dict={
                        "status": "create engine"
                    },
                )
                self.db.execute_sql(update_sql)
            except Exception as e:
                logger.error(f"engine 생성에 실패하였습니다. \n"
                             f"container == {self.container}\n"
                             f"name == {engine[0]}\n"
                             f"module_name == {engine[1]}\n"
                             f"{e}")
                update_sql = update_engine_info(
                    table_name=self.table_name,
                    where_dict={
                        "container_name": self.container,
                        "name": engine[0],
                        "module_name": engine[1],
                    },
                    set_dict={
                        "status": "engine 생성에 실패"
                    }
                )
                self.db.execute_sql(update_sql)

        return obj_list


def import_class(module_name, class_name):
    mod = import_module(module_name)
    load_class = getattr(mod, class_name)
    return load_class
