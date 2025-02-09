# main.py
from fastapi import FastAPI
import uvicorn
from src.routes.routes import router

app = FastAPI()

# Include the routes from the routes module
app.include_router(router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="127.0.0.1", port=3000, reload=True)
