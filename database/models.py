from sqlmodel import SQLModel,Field
from datetime import datetime,timezone


class Anuncios(SQLModel, table=True):
    id: int | None = Field(primary_key=True,default=None)
    anuncio: str = Field()
    descripcion: str = Field()

class Blog(SQLModel, table=True):
    id: int | None = Field(primary_key=True,default=None)
    autor: str = Field()
    titulo: str = Field()
    texto: str = Field()
    fecha: datetime = Field(default_factory= lambda: datetime.now(timezone.utc))
    is_admin: bool = Field(default=False)

class Menu(SQLModel, table=True):
    id: int | None = Field(primary_key=True,default=None)
    tema: str = Field()