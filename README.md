# `GPUQueue` A very simple GPU tool - To run multiple jobs with assigned (limited) GPU resources

It provides very simple and basic function of dynamically utilize given GPUs with a large job array.

### Examples

---
``` python
from gpu_queue import JobSubmitter

job_array = [
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(3)'",
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(2)'",
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(0.5)'",
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(0.5)'",
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(3)'",
    "python -c 'import os, time;print(\"GPU num utilized\",os.environ[\"CUDA_VISIBLE_DEVICES\"]);time.sleep(1)'",
]

J = JobSubmitter(job_array, [0, 1, 2])
J.submit_jobs()
```

```
6 jobs has been saved
GPU num utilized 0
GPU num utilized 2
GPU num utilized 1
GPU num utilized 2
GPU num utilized 2
GPU num utilized 1
all jobs has been run
sucessful jobs: 4

failed jobs: 0
```





This script can be used to automatically identify the GPU that has been released by a newly-ended program.

`gpuqueue` can be directly used in the bash interface, see `bash_demo.sh` for more details.



