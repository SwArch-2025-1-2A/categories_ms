from os import getenv
from dotenv import load_dotenv
from fastapi import FastAPI
from app.db import init_db

# Load environment variables from .env file
load_dotenv()

__version__="0.1.0"

app = FastAPI(
    title = "Categories Microservice",
    description = "Microservice for doing CRUD operations with categories. Used by events, groups and users",
    version=__version__
)

# TODO: 
# 1. Setup CORS middleware
# 2. Add the actual routes here
# 3. Setup and test the PORT env variable properly
# 4. Look into the lifespan context manager, to check if it is necessary or not
# 5. Change the @app.on_event (which is currently deprecated) for something that isn't

@app.get("/ping")
async def ping():
    return "Pong"

@app.on_event("startup")
def on_startup():
    init_db()

if __name__ == "__main__":
    import uvicorn

    port = int(getenv("PORT", 8000))

    uvicorn.run(app, host="0.0.0.0", port=port)
