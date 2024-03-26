from queue import Queue
from time import monotonic as time


try:
    from _queue import Empty
except ImportError:
    class Empty(Exception):
        """Exception raised by Queue.get(block=0)/get_nowait()."""
        pass


class Full(Exception):
    """Exception raised by Queue.put(block=0)/put_nowait()."""
    pass


class SuperQueue(Queue):
    """Queue with arbitray insertion and removal"""

    def put(self, item, block=True, timeout=None, index=None):
        """Put an item into the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until a free slot is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Full exception if no free slot was available within that time.
        Otherwise ('block' is false), put an item on the queue if a free slot
        is immediately available, else raise the Full exception ('timeout'
        is ignored in that case).

        If optional arg 'index' is not None, then item will be inserted at
        specified index.
        """
        with self.not_full:
            if self.maxsize > 0:
                if not block:
                    if self._qsize() >= self.maxsize:
                        raise Full
                elif timeout is None:
                    while self._qsize() >= self.maxsize:
                        self.not_full.wait()
                elif timeout < 0:
                    raise ValueError("'timeout' must be a non-negative number")
                else:
                    endtime = time() + timeout
                    while self._qsize() >= self.maxsize:
                        remaining = endtime - time()
                        if remaining <= 0.0:
                            raise Full
                        self.not_full.wait(remaining)

            self._put(item, index=index)
            self.unfinished_tasks += 1
            self.not_empty.notify()

    def get(self, block=True, timeout=None, index=None):
        """Remove and return an item from the queue.

        If optional args 'block' is true and 'timeout' is None (the default),
        block if necessary until an item is available. If 'timeout' is
        a non-negative number, it blocks at most 'timeout' seconds and raises
        the Empty exception if no item was available within that time.
        Otherwise ('block' is false), return an item if one is immediately
        available, else raise the Empty exception ('timeout' is ignored
        in that case).

        If optional arg index is not None, then item will be retrieved at
        specified index.
        """
        with self.not_empty:
            if not block:
                if not self._qsize():
                    raise Empty
            elif timeout is None:
                while not self._qsize():
                    self.not_empty.wait()
            elif timeout < 0:
                raise ValueError("'timeout' must be a non-negative number")
            else:
                endtime = time() + timeout
                while not self._qsize():
                    remaining = endtime - time()
                    if remaining <= 0.0:
                        raise Empty
                    self.not_empty.wait(remaining)
            item = self._get(index=index)
            self.not_full.notify()
            return item

    def put_nowait(self, item, index=None):
        """Put an item into the queue without blocking.

        Only enqueue the item if a free slot is immediately available.
        Otherwise raise the Full exception.
        """
        return self.put(item, block=False, index=index)

    def get_nowait(self, index=None):
        """Remove and return an item from the queue without blocking.

        Only get an item if one is immediately available. Otherwise
        raise the Empty exception.
        """
        return self.get(block=False, index=None)

    # Put a new item in the queue
    def _put(self, item, index=None):
        if index is None:
            self.queue.append(item)
            return
        self.queue.insert(index, item)

    # Get an item from the queue
    def _get(self, index=None):
        if index is None:
            return self.queue.popleft()
        item = self.queue[index]
        del self.queue[index]
        return item
