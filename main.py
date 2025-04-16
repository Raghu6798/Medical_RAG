from fastapi import FastAPI
from chainlit.utils import mount_chainlit
from loguru import logger
import sys
import os

# Configure loguru
logger.remove()  # Remove default handler
logger.add(
    sys.stderr,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}",
    level="INFO"
)
logger.add(
    "app.log",  # Log to a file
    rotation="10 MB",  # Rotate when the file reaches 10MB
    retention="1 week",  # Keep logs for 1 week
    compression="zip",  # Compress rotated logs
    level="DEBUG"
)

# Create FastAPI app
app = FastAPI()

# Log application startup
logger.info("Starting FastAPI application")
mount_chainlit(app=app, target="/routes/query_route.py", path="/chainlit")
logger.info("Chainlit mounted successfully at /chainlit")

# Add some basic logging middleware
@app.middleware("http")
async def logging_middleware(request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response status: {response.status_code}")
    return response

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting Uvicorn server on 0.0.0.0:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)
