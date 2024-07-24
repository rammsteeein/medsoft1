from fastapi import FastAPI
from celery.result import AsyncResult
from tasks import add
import uvicorn
from celery_app import celery_app


app = FastAPI()


@app.post("/add/{x}/{y}")
def run_add_task(x: int, y: int):
    task = add.delay(x, y)
    return {"ID": task.id}


@app.get("/status/{task_id}")
def get_task_status(task_id: str):
    task_result = AsyncResult(task_id, app=celery_app)
    if task_result.state == 'PENDING':
        return {"status": task_result.state}
    elif task_result.state != 'FAILURE':
        return {"status": task_result.state, "res": task_result.result}
    else:
        return {"status": task_result.state, "res": str(task_result.info)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


#celery -A celery_app worker --loglevel=info
#uvicorn main:app --reload

#$response = Invoke-RestMethod -Uri "http://localhost:8000/add/4/5" -Method Post
#$response

#$response = Invoke-RestMethod -Uri "http://localhost:8000/status/{task_id}" -Method Get
#$response