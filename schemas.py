from typing import List

from pydantic import BaseModel, ConfigDict


class RecipeCreate(BaseModel):
    """
    Схема для создания рецепта.
    """
    name: str
    time_in_minutes: int
    list_of_components: List[str]
    documentation: str


class RecipeListOut(BaseModel):
    """
    Схема для списка рецептов.
    """
    id: int
    name: str
    count_of_watches: int
    time_in_minutes: int

    model_config = ConfigDict(from_attributes=True)


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

    model_config = ConfigDict(from_attributes=True)