from typing import List

from pydantic import BaseModel


class BaseRecipe(BaseModel):
    """
    Общие поля рецепта, которые используются и для входа, и для ответа.
    """
    name: str
    time_in_minutes: int
    list_of_components: List[str]
    documentation: str


class RecipeCreate(BaseRecipe):
    """
    Схема для создания рецепта.
    """
    pass


class RecipeListOut(BaseModel):
    """
    Схема для списка рецептов.
    Отдает только поля, которые нужны на первом экране.
    """

    id: int
    name: str
    count_of_watches: int
    time_in_minutes: int

    class Config:
        from_attributes = True


class RecipeDetailOut(BaseModel):
    """
    Схема для детальной карточки рецепта.
    """

    id: int
    name: str
    time_in_minutes: int
    list_of_components: List[str]
    documentation: str
    count_of_watches: int

    class Config:
        from_attributes = True