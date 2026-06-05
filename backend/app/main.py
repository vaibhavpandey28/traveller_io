from fastapi import FastAPI
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 1. Create an instance of the FastAPI class
app = FastAPI()

# 2. Define a route (GET request to the root URL "/")
@app.get("/")
def read_root():
    logger.info("Reading root endpoint")
    return {"message": "Hello World", "status": "It works!"}

# 3. Define another route with a path parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query_param": q}