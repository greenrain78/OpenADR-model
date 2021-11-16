from logging import getLogger
#
# from src.DB.DB_Adapter import DBAdapter
#
from src.DB.DB_Adapter import DBAdapter

logger = getLogger(__name__)
#
# if __name__ == 'main':
#     logger.info("main")
#
#     test = DBAdapter("testars")
#     sql = f"select * from auth_group"
#     data = test.execute_sql(sql)
#     print(data)

logger.info(f"1234", exc_info=True, stack_info=True)
select_sql = f"select * from auth_group"
db = DBAdapter(name="main db ")

print(db.fetch_data_by_sql(select_sql))
