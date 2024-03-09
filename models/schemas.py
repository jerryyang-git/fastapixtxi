from typing import List, Optional

from pydantic import BaseModel


# Tag Schema
class TagBase(BaseModel):
    name: str
    information: Optional[str] = None


class TagCreate(TagBase):
    pass


class Tag(TagBase):
    id: int
    articles: List["Article"] = []

    class Config:
        from_attributes = True


# Developer Schema
class DeveloperBase(BaseModel):
    name: str
    information: Optional[str] = None
    link: Optional[str] = None


class DeveloperCreate(DeveloperBase):
    pass


class Developer(DeveloperBase):
    id: int
    articles: List["Article"] = []

    class Config:
        from_attributes = True


# FileDlink Schema
class FileDlinkBase(BaseModel):
    classname: str = None
    linkinfo: str = None
    describe: str = None


class FileDlinkCreate(FileDlinkBase):
    pass


class FileDlinkUp(FileDlinkCreate):
    article_id: int


class FileDlink(FileDlinkBase):
    id: int
    article_id: int

    class Config:
        from_attributes = True


# Title Schema
class TitleBase(BaseModel):
    title: str
    official: bool
    olang: str


class TitleCreate(TitleBase):
    pass


class TitleCreateBinding(TitleBase):
    article_title_id: int


class Title(TitleBase):
    id: int
    article_title_id: int

    class Config:
        from_attributes = True


# Article Schema
class ArticleBase(BaseModel):
    content: str
    images: str = None
    alias: Optional[str] = None
    link: Optional[str] = None


class ArticleCreate(ArticleBase):
    title: List[TitleCreate]
    tags: List[TagCreate] = None
    developers: List[DeveloperCreate] = None
    filesdlink: List[FileDlinkCreate] = None


class Article(ArticleBase):
    id: int
    title: List[Title] = []
    developers: List[DeveloperBase] = []
    tags: List[TagBase] = []
    filesdlink: List[FileDlink] = []

    class Config:
        from_attributes = True


# 数据库之外模型
class ObtainAllArticles(BaseModel):
    skip: int
    limit: int = 10


class RemoveTag(BaseModel):
    article_id: int
    label_id: int


class Search(BaseModel):
    q: str


class Vdid(BaseModel):
    id: int
