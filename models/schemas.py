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
        orm_mode = True


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
        orm_mode = True


# FileDlink Schema
class FileDlinkBase(BaseModel):
    classname: str = None
    linkinfo: str = None
    describe: str = None


class FileDlinkCreate(FileDlinkBase):
    pass


class FileDlink(FileDlinkBase):
    id: int
    article_id: int

    class Config:
        orm_mode = True


# Title Schema
class TitleBase(BaseModel):
    title: str
    official: bool
    olang: str


class TitleCreate(TitleBase):
    pass


class Title(TitleBase):
    id: int
    article_id: int

    class Config:
        orm_mode = True


# Article Schema
class ArticleBase(BaseModel):
    content: str
    images: str
    alias: Optional[str] = None
    link: Optional[str] = None


class ArticleCreate(ArticleBase):
    tags: List[TagCreate] = None
    developers: List[DeveloperCreate] = None
    filesdlink: List[FileDlinkCreate] = None
    title: List[TitleCreate] = None


class Article(ArticleBase):
    id: int
    filesdlink: List[FileDlink] = []
    tags: List[TagBase] = []
    developers: List[DeveloperBase] = []
    title: List[Title] = []

    class Config:
        orm_mode = True


# 数据库之外模型
class allArticle(BaseModel):
    skip: int
    limit: int = 10
