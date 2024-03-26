import threading
from functools import wraps
from threading import Thread


def wait_thread(thread_name: str = "submitter", timeout: int = None):
    for t in threading.enumerate():
        if t.name == thread_name:
            t.join(timeout=timeout)


def threaded(_func=None, *, name: str = None, daemon=False):
    """Decorator to run the process in an extra thread."""

    def decorator_thread(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            new_thread = Thread(target=f, args=args, kwargs=kwargs, name=name)
            new_thread.daemon = daemon
            new_thread.start()
            return new_thread

        return wrapper

    if _func is None:
        return decorator_thread
    else:
        return decorator_thread(_func)
