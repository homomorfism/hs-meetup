from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    icon: str | None = None
    slug: str


class Category(CategoryBase):
    id: int

    class Config:
        from_attributes = True
