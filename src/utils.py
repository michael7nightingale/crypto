import time
from logger import logger


def nowTime() -> float:
    return time.time()


def is_over(x: float, y: float, percents: float) -> bool:
    """Is x more than y on percents%"""
    percents_over_x = (y * 100) / x - 100
    return percents_over_x >= percents


def callback(fut):
    try:
        result = fut.result()
    except Exception as e:
        logger.info(str(e))

