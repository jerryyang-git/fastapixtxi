from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from models import models, schemas, crud
from typing import List

from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 查看指定id文章
@app.get("/api/{id}", response_model=schemas.Article)
def get_article(id: int, db: Session = Depends(get_db)):
    db_test = crud.get_article(db, article_id=id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="文章丢失拉w(ﾟДﾟ)w")
    return db_test

# 获取所有文章的路由
@app.post("/api/allatr", response_model=List[schemas.Article])
def read_articles(iaxy:schemas.allArticle, db: Session = Depends(get_db)):
    articles = crud.get_articles(db, iaxy)
    return articles

# 创建文章
@app.post("/api/add", response_model=schemas.Article)
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.upsert_article(db, article)


# 创建标题
@app.post("/api/title",response_model=schemas.Title)
def create_title(title: schemas.TitleCreate,db:Session = Depends(get_db)):
    return crud.create_title(db,title)

@app.post("/api/tag",response_model=schemas.Tag)
def create_tag(tag:schemas.TagCreate,db:Session = Depends(get_db)):
    return crud.create_tag(db,tag)
