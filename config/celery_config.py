import os
from functools import lru_cache
from kombu import Queue


"""
    Route tasks to specific queues based on their name prefix.
    Example: "email_notification_task" -> "email_notification" queue.
    """

def route_task(name, args, kwargs, options, task=None, **kw):
    if ":" in name:
        queue, _ = name.split(":")
        return {"queue": queue}
    return {"queue": "celery"}


class BaseConfig:
    CELERY_BROKER_URL: str = os.environ.get("CELERY_BROKER_URL", "amqp://guest:guest@localhost:5672//")
    CELERY_RESULT_BACKEND: str = os.environ.get("CELERY_RESULT_BACKEND", "rpc://")

    CELERY_TASK_QUEUES: list = (
        # default queue
        Queue("celery"),
        # custom queue
        Queue("email_notification"),
        Queue("gatewayservice"),
        Queue("ocr_service")
    )

    CELERY_TASK_ROUTES = (route_task,)


class DevelopmentConfig(BaseConfig):
    CELERY_TASK_ALWAYS_EAGER = False  # Run tasks asynchronously
    CELERY_TASK_ACKS_LATE = True  # Acknowledge after task execution (avoids losing tasks)
    CELERY_WORKER_CONCURRENCY = int(os.getenv("CELERY_WORKER_CONCURRENCY", 4))  # Worker threads
    config_name = os.environ.get("CELERY_CONFIG", "development")
    

# Singleton Config Getter
@lru_cache()
def get_settings():
    config_cls_dict = {
        "development": DevelopmentConfig,
    }
    config_name = os.environ.get("CELERY_CONFIG", "development")
    config_cls = config_cls_dict[config_name]
    return config_cls()


settings = get_settings()