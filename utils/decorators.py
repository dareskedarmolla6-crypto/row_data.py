import time
import functools
import logging


# =========================
# LOGGING SETUP
# =========================
logger = logging.getLogger("FSE")
logger.setLevel(logging.INFO)


# =========================
# EXECUTION TIME DECORATOR
# =========================
def timer(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        logger.info(f"[TIMER] {func.__name__} took {end - start:.4f}s")
        return result

    return wrapper


# =========================
# RETRY DECORATOR
# =========================
def retry(max_attempts=3, delay=1):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            attempts = 0

            while attempts < max_attempts:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    attempts += 1
                    logger.warning(
                        f"[RETRY] {func.__name__} failed ({attempts}/{max_attempts}): {e}"
                    )
                    time.sleep(delay)

            raise Exception(f"{func.__name__} failed after {max_attempts} attempts")

        return wrapper
    return decorator


# =========================
# SAFE EXECUTION GUARD
# =========================
def safe_execute(default_return=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"[ERROR] {func.__name__}: {e}")
                return default_return

        return wrapper
    return decorator


# =========================
# CONFIDENCE FILTER DECORATOR
# =========================
def require_confidence(min_confidence=60):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            confidence = kwargs.get("confidence", None)

            if confidence is None and len(args) > 1:
                confidence = args[1]

            if confidence is not None and confidence < min_confidence:
                logger.info(
                    f"[BLOCKED] {func.__name__} confidence too low: {confidence}"
                )
                return None

            return func(*args, **kwargs)

        return wrapper
    return decorator


# =========================
# TRADE LOG DECORATOR
# =========================
def trade_logger(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"[TRADE START] {func.__name__}")
        result = func(*args, **kwargs)
        logger.info(f"[TRADE END] {func.__name__}")
        return result

    return wrapper
