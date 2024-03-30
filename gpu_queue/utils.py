import threading
from functools import wraps
from threading import Thread


class _SingletonMeta(type):
    """
    The Singleton class can be implemented in different ways in Python. Some
    possible methods include: base class, decorator, metaclass. We will use the
    metaclass because it is best suited for this purpose.
    """

    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


def wait_thread(thread_name: str = "submitter", timeout: int = None):
    for t in threading.enumerate():
        if t.name == thread_name:
            t.join(timeout=timeout)


def threaded(_func=None, *, name: str = None, daemon=False):
    """Decorator to run the process in an extra thread."""

    def decorator_thread(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            new_thread = Thread(
                target=f, args=args, kwargs=kwargs, name=name, daemon=daemon
            )
            new_thread.start()
            return new_thread

        return wrapper

    if _func is None:
        return decorator_thread
    else:
        return decorator_thread(_func)
