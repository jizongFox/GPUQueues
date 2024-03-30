from gpu_queue import JobSubmitter
from gpu_queue.main import launch_server

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
] * 20
J = JobSubmitter(job_array, [0, 1, 2], wait_second=0, first_time_wait_second=0)

J.submit_jobs()

launch_server(8080)
# worker.join()
