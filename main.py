from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal, engine
from models import models, schemas, crud

# 创建数据库表
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# 挂载后台管理系统


# 依赖项 - 获取数据库连接
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 获取所有文章
@app.post("/articles/all", response_model=List[schemas.Article], tags=['文章'], summary="获取所有文章")
def read_articles(iaxy: schemas.ObtainAllArticles, db: Session = Depends(get_db)):
    articles = crud.post_articles(db, iaxy)
    return articles


# 查看指定id文章
@app.post("/articles", response_model=schemas.Article, tags=['文章'], summary="查看指定 id 文章")
def post_article(id: schemas.Vdid, db: Session = Depends(get_db)):
    db_test = crud.post_article(db, id.id)
    if db_test is None:
        raise HTTPException(status_code=404, detail="文章丢失拉w(ﾟДﾟ)w")
    return db_test


# 创建文章
@app.post("/api/add", response_model=schemas.Article, tags=['文章'],
          summary="创建文章(包含文章tag、title等信息")
def create_article(article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.create_article(db, article)


# 更新指定 id article 内容字段（不包括 tag 等标签）
@app.put("/api//article", response_model=schemas.ArticleBase, tags=['文章'],
         summary="更新指定 id 文章 内容字段（不包括 tag 等标签）")
def update_title(id: schemas.Vdid, article: schemas.ArticleBase, db: Session = Depends(get_db)):
    db_article = crud.update_article_id(db, id.id, article)
    return db_article


# 标签
# 创建Tag标签
@app.post("/api/tag", response_model=schemas.Tag, tags=['标签'], summary="创建 tag")
def create_tag(tag: schemas.TagCreate, db: Session = Depends(get_db)):
    return crud.create_tag(db, tag)


# 更新指定 id tag
@app.put("/tag/edit/{id}", response_model=schemas.Tag, tags=['标签'],
         summary="更新指定 id tag")
def update_developers(id: int, tag: schemas.TagCreate, db: Session = Depends(get_db)):
    db_tag = crud.update_tag_by_id(db, id, tag)
    return db_tag


# 查看指定id tag
@app.post("/tag", response_model=schemas.Tag, tags=['标签'], summary="查看指定 id tag")
def post_tag(id: schemas.Vdid, db: Session = Depends(get_db)):
    db_test = crud.post_tag(db, id.id)
    return db_test


# 创建 filelink 并绑定到一个 文章
@app.post("/api/filelink", response_model=schemas.FileDlinkUp, tags=['标签'], summary="创建 filelink 并绑定到一个 文章")
def create_filelink(filelink: schemas.FileDlinkUp, db: Session = Depends(get_db)):
    return crud.create_filelink(db, filelink)


# 更新指定 id filelink
@app.put("/api/filelink", response_model=schemas.FileDlinkCreate, tags=['标签'],
         summary="更新指定 id filelink")
def update_title(id: schemas.Vdid, filelink: schemas.FileDlinkCreate, db: Session = Depends(get_db)):
    db_filelink = crud.update_fileslink_by_id(db, id.id, filelink)
    return db_filelink


# 创建绑定指定文章 id 的标题
@app.post("/api/add/title", response_model=schemas.TitleCreateBinding, tags=['标签'],
          summary="创建绑定指定文章的标题")
def create_title(title: schemas.TitleCreateBinding, db: Session = Depends(get_db)):
    return crud.create_title(db, title)


# 创建 developers
@app.post("/api/developers", response_model=schemas.Developer, tags=['标签'], summary="创建 developers")
def create_developer(developers: schemas.DeveloperCreate, db: Session = Depends(get_db)):
    return crud.create_developer(db, developers)


# 查看指定id developers
@app.post("/api/developers", response_model=schemas.Developer, tags=['标签'],
          summary="查看指定 id developers")
def post_developer(id: schemas.Vdid, db: Session = Depends(get_db)):
    db_test = crud.post_developer(db, id.id)
    return db_test


# 更新指定 id 的 developers
@app.put("/api/developers/edit", response_model=schemas.Developer, tags=['标签'],
         summary="更新指定 id developers")
def update_developers(id: schemas.Vdid, developers: schemas.DeveloperCreate, db: Session = Depends(get_db)):
    db_title = crud.update_developer_by_id(db, id.id, developers)
    return db_title


# 移除某个 tag 与 指定文章的关联
@app.put("/articles/tags/remove", tags=['remove'], summary="移除某个 tag 与 指定文章的关联")
def remove_tag_from_article(item: schemas.RemoveTag, db: Session = Depends(get_db)):
    removed_tags = crud.remove_tag_from_article(db, item.article_id, item.label_id)
    return removed_tags


# 移除某个 developers 与 指定文章的关联
@app.put("/articles/developers/remove", tags=['remove'], summary="移除某个 developers 与 指定文章的关联")
def remove_developers_from_article(item: schemas.RemoveTag, db: Session = Depends(get_db)):
    removed_developers = crud.remove_developers_from_article(db, item.article_id, item.label_id)
    return removed_developers

    # 删除指定 id 文章及它的标题


@app.delete("/articles/delete", tags=['remove'], summary="删除指定 id 文章及它的标题")
def delete_article(id: schemas.Vdid, db: Session = Depends(get_db)):
    del_article = crud.delarticles(db, id.id)
    return del_article


# 删除指定 id tag
@app.delete("/tag/delete", tags=['remove'], summary="删除指定 id tag")
def delete_tag(id: schemas.Vdid, db: Session = Depends(get_db)):
    del_tag = crud.deltag(db, id.id)
    return del_tag


# 删除指定 id developers
@app.delete("/developers/delete", tags=['remove'], summary="删除指定 id developers")
def delete_developers(id: schemas.Vdid, db: Session = Depends(get_db)):
    del_developers = crud.deldevelopers(db, id.id)
    return del_developers


# 更新指定id标题
@app.put("/api/titles/", response_model=schemas.Title, tags=['文章'], summary="更新指定 id 标题")
def update_title(id: schemas.Vdid, title: schemas.TitleCreate, db: Session = Depends(get_db)):
    db_title = crud.update_title_by_id(db, id.id, title)
    return db_title


# 搜索全部标题和文章别名并返回文章和标题还有别名
@app.post("/search", tags=['搜索'], summary="搜索全部标题和文章别名并返回文章和标题还有别名")
def searchfortitle(search_data: schemas.Search, db: Session = Depends(get_db)):
    articles = crud.searchfortitle(db, search_data)
    return articles


# 搜索 tag
@app.post("/search/tag", tags=['搜索'], summary="搜索全部 tag")
def searchtag(search_data: schemas.Search, db: Session = Depends(get_db)):
    tags = crud.searchtag(db, search_data)
    return tags


# 搜索 developer
@app.post("/search/developer", tags=['搜索'], summary="搜索全部 developer")
def searchdeveloper(search_data: schemas.Search, db: Session = Depends(get_db)):
    developers = crud.searchdeveloper(db, search_data)
    return developers
