from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from Scripts.semantic_concept_search import search_from_query


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class SearchRequest(BaseModel):
    query: str


@app.get("/")
def root():

    return {
        "message": "LeetCodeFind API is running"
    }


@app.post("/search")
def search(request: SearchRequest):

    return search_from_query(
        request.query
    )