# `GPUQueue` A very simple GPU tool - To run multiple jobs with assigned (limited) GPU resources

It provides very simple and basic function of dynamically utilize given GPUs with a large job array. It can be used to automatically identify the GPU that has been released by a newly-ended program.

### Examples

---
`python` interface
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
Output:
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
`gpuqueue` can be directly used in the bash   
`Bash` interface
```bash
#!/usr/bin/env bash

# example of typical machine learning hyper-parameter tuning 
# mean teacher for semi supervised learning

save_dir=cifar10/labeled_sample_4000/augment_img
EMA_decay=0.999

declare -a StringArray=(
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacherbaseline  RegScheduler.max_value=0  Trainer.EMA_decay=${EMA_decay}  "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_0.1      RegScheduler.max_value=0.1  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_1        RegScheduler.max_value=1  Trainer.EMA_decay=${EMA_decay}  "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_10       RegScheduler.max_value=10  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_20       RegScheduler.max_value=20  Trainer.EMA_decay=${EMA_decay} "
"python classify_main.py Trainer.name=MeanTeacherTrainer Config=config/cifar_mt_config.yaml Trainer.save_dir=${save_dir}/meanteacher_50       RegScheduler.max_value=50  Trainer.EMA_decay=${EMA_decay} "
)
# just using 0 and 1 gpus for those jobs
gpuqueue "${StringArray[@]}" --available_gpus 0 1
```


---
### install 
```bash
pip install gpuqueue
```

