from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from datetime import datetime

app = FastAPI()


class Route(BaseModel):
    from_city: str
    to_city: str
    departure: datetime
    arrival: datetime


class Train(BaseModel):
    name: str
    number: str
    routes: List[Route]


trains = [
    Train(
        name="Сапсан",
        number="001А",
        routes=[
            Route(from_city="Москва", to_city="Санкт-Петербург", departure=datetime(2024, 7, 10,
                  9, 0), arrival=datetime(2024, 7, 10, 12, 0))
        ]
    ),
    Train(
        name="Ласточка",
        number="002Б",
        routes=[
            Route(from_city="Москва", to_city="Нижний Новгород", departure=datetime(2024, 7, 12,
                  10, 0), arrival=datetime(2024, 7, 12, 14, 0))
        ]
    ),
    Train(
        name="Скорый Москва-Липецк",
        number="003В",
        routes=[
            Route(from_city="Москва", to_city="Липецк", departure=datetime(2024, 7, 11,
                  11, 0), arrival=datetime(2024, 7, 11, 16, 0))
        ]
    )
]


@app.get("/train/{train_number}", response_model=Train)  #uvicorn second_task:app --reload
def get_train_by_number(train_number: str):
    for train in trains:
        if train.number == train_number:
            return train
    raise HTTPException(status_code=404, detail="Train not found")
