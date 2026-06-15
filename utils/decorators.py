
# fse/utils/decorators.py
import time
import functools
import logging

logger = logging.getLogger("FSE.Decorators")

# =========================
# PERFORMANCE & SAFETY DECORATORS
# =========================

def timer(func):
    """የአፈጻጸም ጊዜን የሚለካ (Performance Monitoring)።"""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        duration = time.perf_counter() - start
        logger.debug(f"[TIMER] {func.__name__} executed in {duration:.4f}s")
        return result
    return wrapper

def retry(max_attempts=3, delay=1):
    """መርህ #11 (Resilience): ለኔትወርክ ስህተቶች ድጋሚ መሞከሪያ።"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"[RETRY] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}")
                    time.sleep(delay)
            logger.error(f"[FATAL] {func.__name__} exhausted {max_attempts} attempts.")
            raise last_exception
        return wrapper
    return decorator

def safe_execute(default_return=None):
    """መርህ #10: የስርዓት ብልሽትን (Crash) የሚከላከል ደህንነት።"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                logger.error(f"[ERROR] {func.__name__} failed: {e}")
                return default_return
        return wrapper
    return decorator

def require_confidence(min_confidence=60):
    """መርህ #4 (Confidence Scoring): ዝቅተኛ ሲግናሎችን ማጣሪያ።"""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # 'confidence' የሚል argument ካለ ወይም በቦታው ካለ መፈተሽ
            conf = kwargs.get("confidence") or (args[1] if len(args) > 1 else 0)
            if conf < min_confidence:
                logger.info(f"[BLOCKED] {func.__name__} suppressed: confidence {conf} < {min_confidence}")
                return None
            return func(*args, **kwargs)
        return wrapper
    return decorator
