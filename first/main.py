from fastapi import FastAPI

app = FastAPI()


@app.get("/api/greeting")
def root(name: str):
    return {"message": f"Hello {name}"}