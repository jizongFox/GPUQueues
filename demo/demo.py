import time

from gpu_queue import JobSubmitter

job_array = [
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.1)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(2.3)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.5)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.5)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.6)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.1)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.5)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.123)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(2.23)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.15)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(0.325)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.12123)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(1.123)\'',
    'python3 -c \'import os, time;print("GPU num utilized",os.environ["CUDA_VISIBLE_DEVICES"]);time.sleep(3.1123232)\'',
] * 20
J = JobSubmitter(job_array, [0], wait_second=0, first_time_wait_second=0)

worker = J.submit(block=False)
time.sleep(10)
J.app.launch_server(8080)
worker.join()
