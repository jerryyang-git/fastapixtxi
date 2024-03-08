from sqlalchemy.orm import Session

from . import models, schemas


# # Article的CRUD操作
# def create_article(db: Session, article: schemas.ArticleCreate):
#     db_article = models.Article(**article.dict())
#     db.add(db_article)
#     db.commit()
#     db.refresh(db_article)
#     return db_article

def upsert_article(db: Session, article_data: schemas.ArticleCreate):
    # 尝试根据ID查找文章
    db_article = db.query(models.Article).filter(models.Article.id == article_data.id).first()

    if db_article:
        # 如果文章存在，更新显式设置的字段
        update_data = article_data.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
    else:
        # 如果文章不存在，创建新的文章
        article_dict = article_data.dict(exclude_unset=True)  # 将 article_data 转换为字典

        db_article = models.Article(**article_dict)  # 使用字典创建 Article 实例

        tags = article_dict.pop('tags', {})
        db_tags = [models.Tag(**tag) for tag in tags]

        db.add_all([db_article, *db_tags])
        db.commit()
        db.refresh(db_article)

    return db_article


# 获取所有文章
def get_articles(db: Session, iaxy: schemas.allArticle):
    return db.query(models.Article).offset(iaxy.skip).limit(iaxy.limit).all()


# 获取文章
def get_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


# CRUD operations for Title
def create_title(db: Session, title: schemas.TitleCreate):
    db_title = models.Title(**title.dict())
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title


# CRUD operations for Tag
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.id == tag_id).first()


# CRUD operations for Developer
def create_developer(db: Session, developer: schemas.DeveloperCreate):
    db_developer = models.Developer(**developer.dict())
    db.add(db_developer)
    db.commit()
    db.refresh(db_developer)
    return db_developer


def get_developer(db: Session, developer_id: int):
    return db.query(models.Developer).filter(models.Developer.id == developer_id).first()


# CRUD operations for FileDlink
def create_file_dlink(db: Session, file_dlink: schemas.FileDlinkCreate, article_id: int):
    db_file_dlink = models.FileDlink(**file_dlink.dict(), article_id=article_id)
    db.add(db_file_dlink)
    db.commit()
    db.refresh(db_file_dlink)
    return db_file_dlink


def get_file_dlink(db: Session, file_dlink_id: int):
    return db.query(models.FileDlink).filter(models.FileDlink.id == file_dlink_id).first()
