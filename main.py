from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

app = FastAPI()


@app.get("/api/greeting")
def root(name: str):
    data = {"message": f"Hello {name}"}
    json_data = jsonable_encoder(data)
    return JSONResponse(content=json_data)