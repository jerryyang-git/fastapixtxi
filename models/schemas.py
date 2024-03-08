from typing import List, Optional
from pydantic import BaseModel

# 数据库之外模型
class allArticle(BaseModel):
    skip:int
    limit:int = 10


# Title Schema
class TitleBase(BaseModel):
    olang: str
    official: bool
    title: str
    article_id: int

# Article Schema
class ArticleBase(BaseModel):
    content: str
    imges: str
    alias: Optional[str] = None
    link: Optional[str] = None
    
class TagBase(BaseModel):
    name: str
    information: Optional[str] = None

class TagCreate(TagBase):
    pass

class ArticleCreate(ArticleBase):
    tags: List[TagBase] = None
    id: int = None

class Article(ArticleBase):
    id: int
    filesdlink:List['FileDlink'] = []
    tags:List['TagBase'] = []
    developers:List['Developer'] = []

    class Config:
        orm_mode = True


# Tag Schema
class TagBase(BaseModel):
    name: str
    information: Optional[str] = None

class TagCreate(TagBase):
    pass

class Tag(TagBase):
    id: int
    articles: List[Article] = []

    class Config:
        orm_mode = True



class TitleCreate(TitleBase):
    pass

class Title(TitleBase):
    id: int

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
    articles: List[Article] = []

    class Config:
        orm_mode = True

# FileDlink Schema
class FileDlinkBase(BaseModel):
    classname: str
    linkinfo: str
    describe: str
    article_id: int

class FileDlinkCreate(FileDlinkBase):
    pass

class FileDlink(FileDlinkBase):
    id: int
    article:List['Article'] = []

    class Config:
        orm_mode = True