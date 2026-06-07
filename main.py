from contextlib import asynccontextmanager
from typing import List
import json

from fastapi import Depends, FastAPI, HTTPException, Path
from sqlalchemy import asc, desc
from sqlalchemy.future import select
from sqlalchemy.orm import Session

import models
import schemas
from database import Base, SessionLocal, engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Выполняет код при старте и завершении приложения.

    До yield:
        - создаёт таблицы в базе данных.

    После yield:
        - освобождает engine.
    """
    Base.metadata.create_all(bind=engine)
    yield
    engine.dispose()


app = FastAPI(lifespan=lifespan)


def get_db():
    """
    Возвращает сессию базы данных для одного запроса.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/recipes", response_model=List[schemas.RecipeListOut])
def get_recipes(db: Session = Depends(get_db)):
    """
    Возвращает список всех рецептов.

    Сортировка:
    - сначала по количеству просмотров по убыванию;
    - при равенстве просмотров по времени готовки по возрастанию.
    """
    stmt = (
        select(models.Recipes)
        .order_by(
            desc(models.Recipes.count_of_watches),
            asc(models.Recipes.time_in_minutes),
        )
    )
    result = db.execute(stmt)
    return result.scalars().all()


@app.get("/recipes/{recipe_id}", response_model=schemas.RecipeDetailOut)
def get_recipe(
    recipe_id: int = Path(..., title="ID recipe for searching"),
    db: Session = Depends(get_db),
):
    """
    Возвращает детальную информацию по одному рецепту.

    Также увеличивает количество просмотров рецепта на 1.
    """
    stmt = select(models.Recipes).where(models.Recipes.id == recipe_id)
    result = db.execute(stmt)
    recipe = result.scalars().first()

    if recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not found")

    recipe.count_of_watches += 1
    db.commit()
    db.refresh(recipe)

    return {
        "id": recipe.id,
        "name": recipe.name,
        "time_in_minutes": recipe.time_in_minutes,
        "list_of_components": json.loads(recipe.list_of_components),
        "documentation": recipe.documentation,
        "count_of_watches": recipe.count_of_watches,
    }


@app.post("/recipes", response_model=schemas.RecipeDetailOut, status_code=201)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    """
    Создаёт новый рецепт и сохраняет его в базу.
    """
    new_recipe = models.Recipes(
        name=recipe.name,
        time_in_minutes=recipe.time_in_minutes,
        list_of_components=json.dumps(recipe.list_of_components, ensure_ascii=False),
        documentation=recipe.documentation,
    )

    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)

    return {
        "id": new_recipe.id,
        "name": new_recipe.name,
        "time_in_minutes": new_recipe.time_in_minutes,
        "list_of_components": json.loads(new_recipe.list_of_components),
        "documentation": new_recipe.documentation,
        "count_of_watches": new_recipe.count_of_watches,
    }