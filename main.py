from logging import getLogger

from src.DB.DB_Adapter import DBAdapter

logger = getLogger(__name__)

if __name__ == 'main':
    logger.info("main")

    test = DBAdapter("testars")
    sql = f"select * from auth_group"
    data = test.execute_sql(sql)
    print(data)
