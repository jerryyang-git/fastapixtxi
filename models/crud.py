from fastapi import HTTPException
from sqlalchemy.orm import Session

from . import models, schemas


# 创建新的文章 & 绑定标签 & FilesLink
def create_article(db: Session, article_data: schemas.ArticleCreate):
    article_dict = article_data.dict(exclude_unset=True)

    # 提取文件链接和标题数据，处理标签
    filelink_data = article_dict.pop("filesdlink", [])
    title_data = article_dict.pop("title", [])
    tags_data = article_dict.pop("tags", [])
    developers_data = article_dict.pop("developers", [])
    # 使用字典创建 Article 实例
    db_article = models.Article(**article_dict)
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
    for title in title_data:
        db_title = models.Title(**title)
        db.add(db_title)
        db.commit()
        db_titles.append(db_title)

    # 添加文章和相关对象到会话中
    db.add(db_article)

    db_article.tags.extend(db_tags)
    db_article.developers.extend(db_developers)
    db_article.filesdlink.extend(db_filelinks)
    db_article.title.extend(db_titles)

    db.commit()
    db.refresh(db_article)

    return db_article


# 获取所有文章（按页&条）
def post_articles(db: Session, iaxy: schemas.ObtainAllArticles):
    return db.query(models.Article).offset(iaxy.skip).limit(iaxy.limit).all()


# 获取指定id文章
def post_article(db: Session, article_id: int):
    return db.query(models.Article).filter(models.Article.id == article_id).first()


# 创建 title 并绑定到指定文章 id
def create_title(db: Session, title: schemas.TitleCreateBinding):
    db_title = models.Title(**title.dict())
    db.add(db_title)
    db.commit()
    db.refresh(db_title)
    return db_title


# 更新指定 ID 标题
def update_title_by_id(db: Session, id: int, title_data: schemas.TitleCreate):
    db_title = db.query(models.Title).filter(models.Title.id == id).first()
    if db_title:
        for key, value in title_data.dict().items():
            setattr(db_title, key, value)
        db.commit()
        db.refresh(db_title)
        return db_title
    else:
        raise HTTPException(status_code=404, detail="标题丢失了 w(ﾟДﾟ)w")


# 删除指定 ID 标题
def delete_title_by_id(db: Session, id: int):
    # 查询数据库中是否有匹配的Title记录
    db_title = db.query(models.Title).filter(models.Title.id == id).first()
    if db_title:
        # 如果找到了匹配的记录，就删除这条记录
        db.delete(db_title)
        # 提交事务，确保删除操作被保存到数据库中
        db.commit()
        # 成功删除后，可以返回一些信息，比如被删除记录的ID
        return {"message": f"ID 为 {id} 的标题已删除 (≧∇≦)b OK"}
    else:
        # 如果没有找到匹配的记录，返回None或者可以返回一个错误信息
        return None


# 更新指定 ID article
def update_article_id(db: Session, id: int, article_data: schemas.ArticleBase):
    db_article = db.query(models.Article).filter(models.Article.id == id).first()
    if db_article:
        for key, value in article_data.dict().items():
            setattr(db_article, key, value)
        db.commit()
        db.refresh(db_article)
        return db_article
    else:
        raise HTTPException(status_code=404, detail="文章丢失力 w(ﾟДﾟ)w")


# 更新指定 ID filelink
def update_fileslink_by_id(db: Session, id: int, filelink_data: schemas.FileDlinkCreate):
    db_filelink_data = db.query(models.FileDlink).filter(models.FileDlink.id == id).first()
    if db_filelink_data:
        for key, value in filelink_data.dict().items():
            setattr(db_filelink_data, key, value)
        db.commit()
        db.refresh(db_filelink_data)
        return db_filelink_data
    else:
        raise HTTPException(status_code=404, detail="链接丢失力 w(ﾟДﾟ)w")


# 创建 filelink 并绑定到一个 文章
def create_filelink(db: Session, filelink_data: schemas.FileDlinkUp):
    # 检查 article_id 是否存在于 article 表中
    article = db.query(models.Article).filter(models.Article.id == filelink_data.article_id).first()
    if not article:
        # 如果 article_id 不存在，抛出 404 错误
        raise HTTPException(status_code=404, detail=f"没有 id 为 {filelink_data.article_id} 的文章哦 (；′⌒`) ")
    db_filelink = models.FileDlink(**filelink_data.dict())
    db.add(db_filelink)
    db.commit()
    db.refresh(db_filelink)
    return db_filelink


# 创建 FileDlink 并关联到指定id（article_id）文章
def create_file_dlink(
        db: Session, file_dlink: schemas.FileDlinkCreate, article_id: int
):
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    if not article:
        # 如果 article_id 不存在，抛出 404 错误
        raise HTTPException(status_code=404, detail=f"没有 id 为 {article_id} 的文章哦 (；′⌒`) ")
    db_file_dlink = models.FileDlink(**file_dlink.dict(), article_id=article_id)
    db.add(db_file_dlink)
    db.commit()
    db.refresh(db_file_dlink)
    return db_file_dlink


# 创建tag
def create_tag(db: Session, tag: schemas.TagCreate):
    db_tag = models.Tag(**tag.dict())
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


# 查看指定id Tag
def post_tag(db: Session, id: int):
    tag_git = db.query(models.Tag).filter(models.Tag.id == id).first()
    if tag_git:
        return tag_git
    else:
        raise HTTPException(status_code=404, detail="TAG 丢失拉 w(ﾟДﾟ)w")


# 更新指定 ID Tag
def update_tag_by_id(db: Session, id: int, tag_data: schemas.TagCreate):
    db_tag = db.query(models.Tag).filter(models.Tag.id == id).first()
    if db_tag:
        for key, value in tag_data.dict().items():
            setattr(db_tag, key, value)
        db.commit()
        db.refresh(db_tag)
        return db_tag
    else:
        raise HTTPException(status_code=404, detail="TAG 丢失力 w(ﾟДﾟ)w")


# 移除某个文章与tag的联系
def remove_tag_from_article(db: Session, article_id: int, label_id: int):
    # 查询指定文章和标签
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    tag = db.query(models.Tag).filter(models.Tag.id == label_id).first()

    if article is None or tag is None:
        return
    # 检查该标签是否与文章关联
    if tag in article.tags:
        # 从文章的标签列表中移除该标签
        article.tags.remove(tag)
        db.commit()
        raise HTTPException(status_code=200,
                            detail=f"成功移除 ID 为 {article_id} 的文章与 ID 为 {label_id} 的标签的关联")
    else:
        raise HTTPException(status_code=400,
                            detail=f"ID 为 {article_id} 的文章未与 ID 为 {label_id} 的标签关联")


# 移除某个文章与 Developer 的联系
def remove_developers_from_article(db: Session, article_id: int, label_id: int):
    # 查询指定文章和标签
    article = db.query(models.Article).filter(models.Article.id == article_id).first()
    developer = db.query(models.Developer).filter(models.Developer.id == label_id).first()

    if article is None or developer is None:
        return
    # 检查该标签是否与文章关联
    if developer in article.developers:
        # 从文章的标签列表中移除该标签
        article.developers.remove(developer)
        db.commit()
        raise HTTPException(status_code=200,
                            detail=f"成功移除 ID 为 {article_id} 的文章与 ID 为 {label_id} 的开发者的关联")
    else:
        raise HTTPException(status_code=400,
                            detail=f"ID 为 {article_id} 的文章未与 ID 为 {label_id} 的开发者关联")


# 删除文章及它的标题
def delarticles(db: Session, id: int):
    delart = db.query(models.Article).filter(models.Article.id == id).first()
    if delart:
        db.delete(delart)
        db.commit()
        raise HTTPException(status_code=200, detail=f"已删除 id 为 {id} 的文章及它的标题")
    else:
        raise HTTPException(status_code=404, detail=f"没有 id 为 {id} 的文章")


# 删除 tag
def deltag(db: Session, id: int):
    deleteart = db.query(models.Tag).filter(models.Tag.id == id).first()
    if deleteart:
        db.delete(deleteart)
        db.commit()
        raise HTTPException(status_code=200, detail=f"已删除 id 为 {id} 的 tag")
    else:
        raise HTTPException(status_code=404, detail=f"没有 id 为 {id} 的 tag")


# 删除 developers
def deldevelopers(db: Session, id: int):
    deletedevelopers = db.query(models.Developer).filter(models.Developer.id == id).first()
    if deletedevelopers:
        db.delete(deletedevelopers)
        db.commit()
        raise HTTPException(status_code=200, detail=f"已删除 id 为 {id} 的 Developer")
    else:
        raise HTTPException(status_code=404, detail=f"没有 id 为 {id} 的 Developer")


# 查看指定id Developer
def post_developer(db: Session, id: int):
    get_dev = (db.query(models.Developer).filter(models.Developer.id == id).first())
    if get_dev:
        return get_dev
    else:
        raise HTTPException(status_code=404, detail="页面丢失拉 w(ﾟДﾟ)w")


# 创建开发组织
def create_developer(db: Session, developer: schemas.DeveloperCreate):
    db_developer = models.Developer(**developer.dict())
    db.add(db_developer)
    db.commit()
    db.refresh(db_developer)
    return db_developer


# 更新指定 ID 的 Developer
def update_developer_by_id(db: Session, id: int, developer_data: schemas.DeveloperCreate):
    # 首先找到对应的标题记录
    db_developer = (db.query(models.Developer)
                    .filter(models.Developer.id == id)
                    .first())
    if db_developer:
        # 如果找到了，更新数据
        for key, value in developer_data.dict().items():
            setattr(db_developer, key, value)
        db.commit()
        db.refresh(db_developer)
        return db_developer
    else:
        raise HTTPException(status_code=404, detail="developers 丢失了 (ο´･д･)??")


# 搜索 tag
def searchtag(db: Session, search_data: schemas.Search):
    tags = (db.query(models.Tag)
            .filter(models.Tag.name.ilike(f"%{search_data.q}%"))
            .all())
    return tags


# 搜索 developer
def searchdeveloper(db: Session, search_data: schemas.Search):
    developer = (db.query(models.Developer)
                 .filter((models.Developer.name.ilike(f"%{search_data.q}%")) |
                         (models.Developer.information.ilike(f"%{search_data.q}%")))
                 .all())
    return developer


# 搜索全部标题和文章别名并返回文章和标题还有别名
def searchfortitle(db: Session, search_data: schemas.Search):
    titles = (db.query(models.Title).join(models.Article)
              .filter((models.Title.title.ilike(f"%{search_data.q}%")) |
                      (models.Article.alias.ilike(f"%{search_data.q}%")))
              .all())
    articles_dict = {}
    # 遍历搜索到的标题，并获取对应的文章以及标题
    for title in titles:
        article = title.article
        # 如果文章 ID 不在字典中，或者文章在字典中但 official 为 false，则添加到字典中
        if article.id not in articles_dict or (
                article.id in articles_dict and not articles_dict[article.id]["official"]):
            articles_dict[article.id] = {
                "article_title_id": title.article_title_id,
                "olang": title.olang,
                "title": title.title,
                "id": title.id,
                "official": title.official,
                "article": {
                    "id": article.id,
                    "alias": article.alias,
                    "content": article.content,
                    "images": article.images,
                    "link": article.link
                }
            }
    # 返回字典的值列表
    return list(articles_dict.values())
