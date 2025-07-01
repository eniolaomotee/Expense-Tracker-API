from logging.config import dictConfig

def configure_logging()-> None:
    dictConfig(
        {
            "version":1,
            "disable_existing_loggers":False,
            "formatters":{
                "console":{
                    "class":"logging.Formatter",
                    "datefmt":"%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ | %(name)s:%(lineno)d - %(message)s",
                },
                "file":{
                    "class":"pythonjsonlogger.jsonlogger.JsonFormatter",
                    "datefmt": "%Y-%m-%d %H:%M:%S",
                    "format": "%(asctime)s.%(msecs)03dZ %(levelname)-8s | %(name)s:%(lineno)d - %(message)s",
                }
            },
            "handlers": {
                "default":{
                    "class": "rich.logging.RichHandler",
                    "level":"DEBUG",
                    "formatter":"console"
                },
                "rotating-file":{
                    "class": "logging.handlers.RotatingFileHandler",
                    "level":"DEBUG",
                    "formatter":"file",
                    "filename":"expenses.log",
                    "maxBytes": 10 * 1024 * 1024,
                    "backupCount": 2,
                    "encoding": "utf-8",
                }
            },
            "loggers":{
                "uvicorn":{
                    "handlers": ["default", "rotating-file"],
                    "level": "INFO"
                },
                "databases":{
                    "handlers": ["default"],
                    "level":"WARNING",
                },
            "root": {
                "handlers": ["default", "rotating-file"], 
                "level":"DEBUG"
            }
            }
        }
        
    )