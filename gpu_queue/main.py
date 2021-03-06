import argparse
import time
from queue import Queue, Empty
from subprocess import run
from typing import List

Job_Type = str
Job_Array_Type = List[Job_Type]
import os
from functools import wraps
import threading
from threading import Thread
from contextlib import contextmanager
import re

try:
    from stdout_writer import log_writer
except ModuleNotFoundError:
    from .stdout_writer import log_writer


@contextmanager
def wait_thread_ends(thread_name="submitter"):
    yield
    for t in threading.enumerate():
        if t.name == thread_name:
            t.join()


def threaded(_func=None, *, name="", daemon=False):
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


def get_args():
    parser = argparse.ArgumentParser(description="Dynamic gpu job submitter")
    parser.add_argument("jobs", nargs="+", type=str)
    parser.add_argument("--available_gpus", type=str, nargs="+", default=["0"], metavar="N",
                        help="Available GPUs")
    parser.add_argument("--save_dir", type=str, default="log", help="save_dir for log files")
    args = parser.parse_args()
    # print(f"input args:%s" % args)
    print(f"There are {len(args.jobs)} jobs")
    return args


# here using python os.environment to set global variables.
# you have one worker to launch job and get variables
# you have one monitor to choose which variable to assign to the next job
class JobSubmitter:

    def __init__(self, job_array: Job_Array_Type, available_gpus: List[str] = ["0"], save_dir="log",
                 verbose=False) -> None:
        super().__init__()
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"
        self.job_array = job_array
        self.available_gpus = available_gpus
        self.job_queue = Queue()
        self.verbose = verbose
        self.save_dir = save_dir
        for job in self.job_array:
            self.job_queue.put(job)
        self.gpu_queue = Queue()
        for gpu in self.available_gpus:
            self.gpu_queue.put(gpu)
        print("%d jobs has been loaded" % len(self.job_array))
        self.result_dict = {}

    def submit_jobs(self):
        while True:

            try:
                job = self.job_queue.get(timeout=1)  # if it is going te be empty, end the program
                gpu = self.gpu_queue.get(timeout=None, block=True)  # this will wait forever
                self._process_daemeon(job, gpu)
                time.sleep(2)

            except TimeoutError:
                pass
            except Empty:  # the jobs are done
                with wait_thread_ends(thread_name="submitter"):
                    pass
                print("all jobs has been run")
                s_dict = {k: v for k, v in self.result_dict.items() if v == 0}
                print(f"sucessful jobs: {len(s_dict)}")
                if self.verbose:
                    self._print(s_dict)

                f_dict = {k: v for k, v in self.result_dict.items() if v != 0}
                print(f"failed jobs: {len(f_dict)}")
                if self.verbose:
                    self._print(f_dict)
                break

    @threaded(daemon=False, name="submitter")
    def _process_daemeon(self, job, gpu):
        new_environment = os.environ.copy()
        new_environment["CUDA_VISIBLE_DEVICES"] = str(gpu)
        with log_writer(job, save_dir=self.save_dir) as writer:
            result_code = run(job, shell=True, env=new_environment, stdout=writer)
        self.result_dict[job] = result_code.returncode
        # Recycling GPU num
        self.gpu_queue.put(gpu)

    def _print(self, result_dict):
        for k, v in result_dict.items():
            k = ' '.join(re.split(' +|\n+', k)).strip()
            print(f"Job:\n{k}")
            print("result_code", v)


def main():
    args = get_args()
    jobmanager = JobSubmitter(args.jobs, args.available_gpus, verbose=False, save_dir=args.save_dir)
    jobmanager.submit_jobs()


if __name__ == "__main__":
    main()
