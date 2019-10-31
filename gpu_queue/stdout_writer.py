from datetime import datetime
from pathlib import Path
import time

class log_writer:
    def __init__(self, job_script: str, save_dir="log") -> None:
        super().__init__()
        self.job_script = job_script
        self.launch_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.save_dir = save_dir
        if self.save_dir:
            Path(save_dir).mkdir(exist_ok=True, parents=True)
        print(f"Job {self.job_script}->`job_{self.launch_time}.log`")
        time.sleep(1)

    def __enter__(self):
        if self.save_dir:
            self.f = open(f"{str(Path(self.save_dir) / ('job_' + self.launch_time + '.log'))}", "w")
        else:
            self.f = open(f"job_{self.launch_time}.log")
        self.f.writelines(self.job_script)
        self.f.writelines(f"\nlaunched at {self.launch_time}\n")
        self.f.writelines("output log:\n")
        return self.f

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.f.close()
