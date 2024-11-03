from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session, select, update
from ..models import Anuncios
from ..db_config import get_session


rt = APIRouter(prefix="/anuncios", tags=["anuncios"])


@rt.post("/", response_model=Anuncios, status_code=201)
async def create_anuncio(
    session: Annotated[Session, Depends(get_session)], anuncio: Anuncios
):
    session.add(anuncio)
    session.commit()
    session.refresh(anuncio)
    return anuncio


@rt.get("/", response_model=list[Anuncios])
async def get_anuncios(session: Annotated[Session, Depends(get_session)]):
    anuncios = session.exec(select(Anuncios)).all()
    return anuncios


@rt.get("/{id}", response_model=Anuncios)
async def get_anuncio_by_id(session: Annotated[Session, Depends(get_session)], id: int):
    anuncio = session.exec(select(Anuncios).where(Anuncios.id == id)).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Ese anuncio no existe")
    return anuncio


@rt.put("/{id}", response_model=Anuncios)
async def update_anuncio(
    session: Annotated[Session, Depends(get_session)], id: int, anuncio: Anuncios
):
    anuncio_db = session.exec(select(Anuncios).where(Anuncios.id == id)).first()
    if not anuncio_db:
        raise HTTPException(status_code=404, detail="Ese anuncio no existe")
    session.exec(
        update(Anuncios)
        .where(Anuncios.id == id)
        .values({"anuncio": anuncio.anuncio, "descripcion": anuncio.descripcion})
    )
    session.commit()
    anuncio.id = id
    return anuncio


@rt.delete("/{id}", response_model=str)
async def delete_anuncio(session: Annotated[Session, Depends(get_session)], id: int):
    anuncio = session.exec(select(Anuncios).where(Anuncios.id == id)).first()
    if not anuncio:
        raise HTTPException(status_code=404, detail="Ese anuncio no existe")
    session.delete(anuncio)
    session.commit()
    return "Anuncio eliminado"
