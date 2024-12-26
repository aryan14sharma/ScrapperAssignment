import uvicorn
from fastapi import FastAPI, Depends, HTTPException,status, APIRouter

from logic.scraper import ProductScraper
from storage import local_storage, redis
from auth.token import verify_token

app = FastAPI()
router = APIRouter()

local_storage_client = local_storage.LocalStorage()
redis_storage_client = redis.RedisStorage()


@router.post("/scrape", dependencies=[Depends(verify_token)])
def scrape_catalogue(pages: int = 1, proxy: str = None):
    try:
        scraper = ProductScraper(pages_limit=pages, proxy=proxy,storage=local_storage_client,cache_storage= redis_storage_client)
        results = scraper.scrape()
        return {"message": f"Scraped {results['total_products']} products successfully."}
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))



app.include_router(router)

if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=False, 
                workers=1, limit_concurrency=5, limit_max_requests=5)