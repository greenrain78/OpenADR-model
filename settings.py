import os

from src.Utils.env.env_import import setting_dev_env, get_env_none

DB_NickName = os.environ.get('DB_NICKNAME')
DATABASES = {
    # docker-compose 에서 직접 기입
    'direct': {
        "database": os.environ.get('DB_NAME'),
        "user": os.environ.get('DB_USER'),
        "password": os.environ.get('DB_PASSWORD'),
        "host": os.environ.get('DB_HOST'),
        "port": os.environ.get('DB_PORT'),
    },
    # 로컬에서 사용하는 DB
    'local': {
        "database": 'openadr',
        "user": 'user',
        "password": '1234',
        "host": "127.0.0.1",
        "port": 11100,
    },
    # docker 내에서 연결
    'server_on_docker': {
        "database": 'openadr',
        "user": 'user',
        "password": '1234',
        "host": 'db',
        "port": 5432,
    },
    'aws': {
        "database": 'openadr',
        "user": 'user',
        "password": '1234',
        "host": "3.38.129.72",
        "port": 11100,
    },
}
# 중요한 설정변수 변경 금지
IS_DB_TEST_SKIP = True  # DB를 사용하는 테스트 코드 실행 여부

# 테스트 설정 변수 반영
IS_RUN_TEST = setting_dev_env('IS_RUN_TEST', default=True)
IS_TEST_ALL = setting_dev_env('IS_TEST_ALL', default=True)

IS_MAIN_RUNNING = setting_dev_env('IS_MAIN_RUNNING', default=True)
MAIN_INTERVAL = setting_dev_env('MAIN_INTERVAL', default=600)
IS_SQL_ECHO = setting_dev_env('IS_SQL_ECHO', default=False)

IS_RUN_SCHEDULER = setting_dev_env('IS_RUN_SCHEDULER', default=True)
ECHO_DB_SETTING = setting_dev_env('ECHO_DB_SETTING', default=True)


def return_settings():
    return {
        'IS_SERVER': get_env_none('IS_SERVER'),
        "DB_NickName": DB_NickName,
        # "DATABASES": DATABASES,   # DB 정보는 생략
        "IS_DB_TEST_SKIP": IS_DB_TEST_SKIP,
        "IS_RUN_TEST": IS_RUN_TEST,
        "IS_TEST_ALL": IS_TEST_ALL,
        "IS_MAIN_RUNNING": IS_MAIN_RUNNING,
        "MAIN_INTERVAL": MAIN_INTERVAL,
        "IS_SQL_ECHO": IS_SQL_ECHO,
        "IS_RUN_SCHEDULER": IS_RUN_SCHEDULER,
        "ECHO_DB_SETTING": ECHO_DB_SETTING,
    }
