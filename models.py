from sqlalchemy import Column, Integer, String, Text

from database import Base


class Recipes(Base):
    """
    ORM-модель рецепта.

    Хранит:
    - название,
    - количество просмотров,
    - время готовки,
    - список ингредиентов в виде JSON-строки,
    - текст описания.
    """

    __tablename__ = "recipes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    count_of_watches = Column(Integer, index=True, default=0, nullable=False)
    time_in_minutes = Column(Integer, index=True, nullable=False)
    list_of_components = Column(Text, nullable=False)
    documentation = Column(Text, nullable=False)