import typing

from fastapi import FastAPI

if typing.TYPE_CHECKING:
    from gpu_queue.main import JobSubmitter

app = FastAPI()
app.submitter: "JobSubmitter"


@app.get("/")
async def root():
    return f"{app.submitter.cur_job}/{len(app.submitter.job_array)}"


@app.get("/liveness/", status_code=200)
def liveness_check():
    return "Liveness check succeeded."


@app.get("/readiness/", status_code=200)
def readiness_check():
    return "Readiness check succeeded."


@app.get("/startup/", status_code=200)
def startup_check():
    return "Startup check succeeded."


@app.get("/update_gpu/{gpus}")
async def update_gpu(gpus):
    if any([x for x in gpus if not x.isdigit()]):
        return "Invalid GPU number"

    app.submitter.update_available_gpus(list(gpus))

    return f"okay, updated to {gpus}"
