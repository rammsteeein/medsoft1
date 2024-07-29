from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from celery.result import AsyncResult
from tasks import transcribe_audio_task

app = FastAPI()


class TranscriptionResponse(BaseModel):
    task_id: str


@app.post("/transcribe", response_model=TranscriptionResponse)
async def transcribe(file: UploadFile = File(...)):
    audio_path = f"temp_{file.filename}"
    with open(audio_path, "wb") as f:
        f.write(await file.read())

    task = transcribe_audio_task.delay(audio_path)

    return {"task_id": task.id}


@app.get("/result/{task_id}")
async def get_result(task_id: str):
    task_result = AsyncResult(task_id)

    if task_result.state == 'PENDING':
        return {"status": "Pending", "result": None}
    elif task_result.state == 'STARTED':
        return {"status": "Processing", "result": None}
    elif task_result.state == 'SUCCESS':
        return {"status": task_result.state, "result": task_result.result}
    elif task_result.state == 'FAILURE':
        return {"status": task_result.state, "result": task_result.result}
    else:
        raise HTTPException(status_code=500, detail="Task failed")


#uvicorn main:app --reload
#celery -A tasks worker --loglevel=info --concurrency=1