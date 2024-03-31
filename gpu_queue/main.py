import argparse
import os
import re
import time
import typing as t
from queue import Queue, Empty
from subprocess import run
from threading import Lock, Thread
from loguru import logger
from gpu_queue.utils import wait_thread, threaded, _SingletonMeta

try:
    from stdout_writer import log_writer
except ModuleNotFoundError:
    from .stdout_writer import log_writer
from gpu_queue.web import App

locker = Lock()


def get_args():
    parser = argparse.ArgumentParser(description="Dynamic gpu job submitter")
    parser.add_argument("jobs", nargs="+", type=str)
    parser.add_argument(
        "--available_gpus",
        type=str,
        nargs="+",
        default=["0"],
        metavar="N",
        help="Available GPUs",
    )
    parser.add_argument(
        "--save_dir", type=str, default="log", help="save_dir for log files"
    )
    args = parser.parse_args()
    # print(f"input args:%s" % args)
    print(f"There are {len(args.jobs)} jobs")
    return args


# here using python os.environment to set global variables.
# you have one worker to launch job and get variables
# you have one monitor to choose which variable to assign to the next job
class JobSubmitter(metaclass=_SingletonMeta):
    def __init__(
        self,
        job_array: str | t.Sequence[str],
        available_gpus: str | int | t.List[str | int],
        save_dir="log",
        verbose=False,
        wait_second: int = 3,
        first_time_wait_second: int = None,
    ) -> None:
        os.environ["CUDA_DEVICE_ORDER"] = "PCI_BUS_ID"

        if isinstance(job_array, str):
            job_array = [job_array]
        if isinstance(available_gpus, (str, int)):
            available_gpus = [available_gpus]

        self.job_array = job_array
        self.available_gpus = available_gpus

        self.job_queue = Queue()
        self.verbose = verbose
        self.save_dir = save_dir

        for job in self.job_array:
            self.job_queue.put(job)

        self.gpu_queue_id = 0
        self.gpu_queue = Queue()

        for gpu in self.available_gpus:
            self.gpu_queue.put([gpu, self.gpu_queue_id])

        print("%d jobs has been loaded" % len(self.job_array))
        self.result_dict = {}
        self.wait_second = wait_second
        self.first_job_wait_second = first_time_wait_second or wait_second

        self.cur_job = 0
        self.app = App(self)

    def __submit_jobs(self):

        while True:
            try:
                job = self.job_queue.get(
                    timeout=1
                )  # if it is going te be empty, end the program
                with locker:
                    gpu = self.gpu_queue.get(
                        timeout=None, block=True
                    )  # this will wait forever
                self._process_daemon(job, gpu)
                time.sleep(
                    self.wait_second if self.cur_job > 0 else self.first_job_wait_second
                )
                self.cur_job += 1

            except Empty:  # the jobs are done
                break
        logger.info("All jobs has been submitted")
        wait_thread(thread_name="process_daemon")
        print("all jobs has been run")
        s_dict = {k: v for k, v in self.result_dict.items() if v == 0}
        print(f"successful jobs: {len(s_dict)}")
        if self.verbose:
            self._print(s_dict)

        f_dict = {k: v for k, v in self.result_dict.items() if v != 0}
        print(f"failed jobs: {len(f_dict)}")
        if self.verbose:
            self._print(f_dict)

    @t.overload
    def submit(self, block: bool = True) -> None:
        ...

    @t.overload
    def submit(self, block: bool = False) -> Thread:
        ...

    def submit(self, block: bool = True) -> None | Thread:
        if block:
            return self.__submit_jobs()
        logger.warning(
            "submitting jobs in a thread, please call .join() at the end of the script"
        )
        return threaded(self.__submit_jobs, daemon=False)()

    def submit_jobs(self):
        return self.submit(block=True)

    def update_available_gpus(self, available_gpus: str | int | t.List[str | int]):
        with locker:
            logger.info(f"Updating available GPUs to {available_gpus}")
            self.gpu_queue_id += 1
            self._wait_until_gpu_consumed()
            # logger.debug("creating new queue")
            gpu_queue = Queue()
            for gpu in available_gpus:
                gpu_queue.put((gpu, self.gpu_queue_id))
            self.available_gpus = available_gpus
            self.gpu_queue = gpu_queue

    def _wait_until_gpu_consumed(self):
        while not self.gpu_queue.empty():
            time.sleep(0.1)
            with locker:
                time.sleep(0.1)

    @threaded(daemon=False, name="process_daemon")
    def _process_daemon(self, job, gpu_message):
        (gpu, gpu_queue_id) = gpu_message
        new_environment = os.environ.copy()
        new_environment["CUDA_VISIBLE_DEVICES"] = str(gpu)
        # with log_writer(job, save_dir=self.save_dir) as writer:
        result_code = run(
            job,
            shell=True,
            env=new_environment,
        )
        self.result_dict[job] = result_code.returncode
        # Recycling GPU num
        if gpu_queue_id == self.gpu_queue_id:
            # logger.debug(f"Recycling GPU {gpu}")
            self.gpu_queue.put((gpu, self.gpu_queue_id))

    @staticmethod
    def _print(result_dict):
        for k, v in result_dict.items():
            k = " ".join(re.split(" +|\n+", k)).strip()
            print(f"Job:\n{k}")
            print("result_code", v)
