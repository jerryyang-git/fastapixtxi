from sqlalchemy import Table, Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


# 文章表
class Article(Base):
    __tablename__ = "article"

    id = Column(Integer, primary_key=True, unique=True)
    content = Column(String(2048))
    images = Column(String(1024))
    alias = Column(String, index=True)
    link = Column(String(5120))

    title = relationship("Title", back_populates="article", cascade="all, delete")
    filesdlink = relationship("FileDlink", back_populates="article", cascade="all, delete")
    tags = relationship("Tag", secondary='article_tag_association', back_populates="articles")
    developers = relationship("Developer", secondary="article_developer_association", back_populates="articles")


# 文章其他标题 表
class Title(Base):
    __tablename__ = "title"

    id = Column(Integer, unique=True, primary_key=True)
    article_title_id = Column(Integer, ForeignKey('article.id'))
    olang = Column(String(255))
    official = Column(Boolean)
    title = Column(String, index=True)

    article = relationship("Article", back_populates="title")


# 标签表
class Tag(Base):
    __tablename__ = "tag"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255), index=True)
    information = Column(String(1024))

    articles = relationship("Article", secondary="article_tag_association", back_populates="tags")


# 开发团队表
class Developer(Base):
    __tablename__ = "developer"

    id = Column(Integer, primary_key=True, unique=True)
    name = Column(String(255))
    information = Column(String(1024))
    link = Column(String(5120))

    articles = relationship("Article", secondary="article_developer_association", back_populates="developers")


# 下载链接信息表
class FileDlink(Base):
    __tablename__ = "fileslink"

    id = Column(Integer, primary_key=True, unique=True)
    article_id = Column(Integer, ForeignKey("article.id"))
    classname = Column(String(255))
    linkinfo = Column(String(5120))
    describe = Column(String(255))

    article = relationship("Article", back_populates="filesdlink")


# 中间表定义
article_developer_association = Table(
    'article_developer_association', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id')),
    Column('developer_id', Integer, ForeignKey('developer.id'))
)

article_tag_association = Table(
    'article_tag_association', Base.metadata,
    Column('article_id', Integer, ForeignKey('article.id'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tag.id'), primary_key=True)
)
