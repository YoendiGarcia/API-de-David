from fastapi import FastAPI
# from .db_config import create_db_and_tables
from routes import anuncios, blogs, menu
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


# @app.get("/")
# def root():
#     create_db_and_tables()
#     return "Tables created"


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
