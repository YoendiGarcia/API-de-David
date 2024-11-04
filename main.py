from fastapi import FastAPI
from database.db_config import create_db_and_tables
from routes import anuncios, blogs, menu
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os


app = FastAPI()


@app.get("/")
def root():
    create_db_and_tables()
    return "Tables created"


app.include_router(anuncios.rt)
app.include_router(blogs.rt)
app.include_router(menu.rt)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  
    uvicorn.run(app, host="0.0.0.0", port=port)
