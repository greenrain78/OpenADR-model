main_loggers_config = {
    "": {  # 모든 로그는 db에 저장
        "level": "DEBUG",
        "handlers": ["db"],
    },
    "__main__": {
        "level": "INFO",
        "handlers": ["console"],
        # "handlers": ["console", "db"],
        # "propagate": False,  # db 연결시 중복 제거
    },
}
