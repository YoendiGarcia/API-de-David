from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated
from sqlmodel import Session, select, update
from database.models import Blog
from database.db_config import get_session


rt = APIRouter(prefix="/blogs", tags=["blogs"])


@rt.post("/", response_model=Blog, status_code=201)
async def create_blog(session: Annotated[Session, Depends(get_session)], blog: Blog):
    session.add(blog)
    session.commit()
    session.refresh(blog)
    return blog


@rt.get("/", response_model=list[Blog])
async def get_blogs(session: Annotated[Session, Depends(get_session)]):
    blogs = session.exec(select(Blog)).all()
    return blogs


@rt.get("/{id}", response_model=Blog)
async def get_blog_by_id(session: Annotated[Session, Depends(get_session)], id: int):
    blog = session.exec(select(Blog).where(Blog.id == id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Ese blog no existe")
    return blog


@rt.put("/{id}", response_model=Blog)
async def update_blog(
    session: Annotated[Session, Depends(get_session)], id: int, blog: Blog
):
    blog_db = session.exec(select(Blog).where(Blog.id == id)).first()
    if not blog_db:
        raise HTTPException(status_code=404, detail="Ese blog no existe")
    session.exec(
        update(Blog)
        .where(Blog.id == id)
        .values({"autor": blog.autor, "titulo": blog.titulo, "texto": blog.texto})
    )
    session.commit()
    blog.id = id
    return blog


@rt.delete("/{id}", response_model=str)
async def delete_blog(session: Annotated[Session, Depends(get_session)], id: int):
    blog = session.exec(select(Blog).where(Blog.id == id)).first()
    if not blog:
        raise HTTPException(status_code=404, detail="Ese blog no existe")
    session.delete(blog)
    session.commit()
    return "Blog eliminado"
