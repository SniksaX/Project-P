from fastapi import FastAPI
from src.routers import movies_r, users_r
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from src.core.limiter import limiter
from src.core.config import settings
import uvicorn
from src.routers import auth
from slowapi import _rate_limit_exceeded_handler

app = FastAPI()
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(auth.router)
app.include_router(users_r.router)
app.include_router(movies_r.router)

if __name__ == "__main__":
    uvicorn.run('main:app', host="0.0.0.0", port=3000, reload=True)
