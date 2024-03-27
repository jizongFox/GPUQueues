import time
from threading import Thread

from gpu_queue import JobSubmitter

job_array = [
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.1)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(2.3)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.5)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.5)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.6)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.1)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.5)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.123)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(2.23)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.15)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.325)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.12123)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.123)\'',
    'python -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.1123232)\'',
] * 2
J = JobSubmitter(job_array, [0, 1, 2], wait_second=0, first_time_wait_second=0)
worker = Thread(target=J.submit_jobs, args=())
worker.start()
# J.submit_jobs()
time.sleep(3)
J.update_available_gpus([8, 8, 8])
worker.join()
