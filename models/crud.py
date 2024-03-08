from sqlalchemy.orm import Session

from . import models, schemas


# # Article的CRUD操作
# def create_article(db: Session, article: schemas.ArticleCreate):
#     db_article = models.Article(**article.dict())
#     db.add(db_article)
#     db.commit()
#     db.refresh(db_article)
#     return db_article

# 创建新的文章or绑定标签


def create_article(db: Session, article_data: schemas.ArticleCreate):
    article_dict = article_data.dict(exclude_unset=True)
    # 处理标签
    tags_data = article_dict.pop("tags", [])
    developers_data = article_dict.pop("developers", [])

    # 提取文件链接和标题数据
    filelink_data = article_dict.pop("filesdlink", [])
    print(filelink_data)
    title_data = article_dict.pop("title", [])
    print(title_data)

    db_article = models.Article(**article_dict)  # 使用字典创建 Article 实例
    # 创建并关联标签
    db_tags = []
    for tag_data in tags_data:
        db_tag = db.query(models.Tag).filter_by(name=tag_data["name"]).first()
        if not db_tag:
            db_tag = models.Tag(**tag_data)
            db.add(db_tag)
            db.commit()
        db_tags.append(db_tag)

    # 创建并关联开发者
    db_developers = []
    for developer_data in developers_data:
        db_developer = (
            db.query(models.Developer).filter_by(name=developer_data["name"]).first()
        )
        if not db_developer:
            db_developer = models.Developer(**developer_data)
            db.add(db_developer)
            db.commit()
        db_developers.append(db_developer)

    # 创建并关联文件链接
    db_filelinks = []
    for filelink in filelink_data:
        db_filelink = models.FileDlink(**filelink)
        db.add(db_filelink)
        db.commit()
        db_filelinks.append(db_filelink)

    # 创建并关联标题
    db_titles = []
    for titles in title_data:
        db_title = models.Title(**titles)
        db.add(db_title)
        db.commit()
        db_titles.append(db_title)

    # 添加文章和相关对象到会话中
    db.add(db_article)

    db_article.tags.extend(db_tags)
    db_article.developers.extend(db_developers)
    db_article.titles.extend(db_titles)
    db_article.filesdlink.extend(db_filelinks)

    db.commit()
    db.refresh(db_article)

    return db_article


# 获取所有文章（按页）
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
    return (
        db.query(models.Developer).filter(models.Developer.id == developer_id).first()
    )


# CRUD operations for FileDlink
def create_file_dlink(
        db: Session, file_dlink: schemas.FileDlinkCreate, article_id: int
):
    db_file_dlink = models.FileDlink(**file_dlink.dict(), article_id=article_id)
    db.add(db_file_dlink)
    db.commit()
    db.refresh(db_file_dlink)
    return db_file_dlink


def get_file_dlink(db: Session, file_dlink_id: int):
    return (
        db.query(models.FileDlink).filter(models.FileDlink.id == file_dlink_id).first()
    )
