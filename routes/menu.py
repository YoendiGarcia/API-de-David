from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session, select, update
from ..models import Menu
from ..db_config import get_session


rt = APIRouter(prefix="/menu", tags=["menu"])


@rt.post("/", response_model=Menu, status_code=201)
async def create_menu(session: Annotated[Session, Depends(get_session)], menu: Menu):
    session.add(menu)
    session.commit()
    session.refresh(menu)
    return menu


@rt.get("/", response_model=Menu)
async def get_menu(session: Annotated[Session, Depends(get_session)], id: int = 1):
    menu = session.get(Menu, id)
    if not menu:
        raise HTTPException(status_code=404, detail="Aun no existe el menu")
    return menu


@rt.put("/", response_model=Menu)
async def update_menu(
    session: Annotated[Session, Depends(get_session)], menu: Menu, id: int = 1
):
    menu_db = session.get(Menu, id)
    if not menu_db:
        raise HTTPException(status_code=404, detail="Aun no existe el menu")
    session.exec(update(Menu).where(Menu.id == id).values({"tema": menu.tema}))
    session.commit()
    menu.id = id
    return menu
