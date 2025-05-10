from fastapi import FastAPI
from pydantic import BaseModel

from suumo_mcp.suumo_scraper import scrape_suumo_list


app = FastAPI()

@app.get("/")
def root():
    return {"message": "suumo mcp server is running"} 

class SuumoRequest(BaseModel):
    url: str


@app.post("/suumo/list")
def get_suumo_list(body: SuumoRequest):
    """
    SUUMOの賃貸リストを取得する
    """
    return scrape_suumo_list(body.url)
