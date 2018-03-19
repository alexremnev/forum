from sqlalchemy import func

from app.models.post import Post


class PostService:

    def __init__(self, session):
        self.session = session

    def list(self, search, page, page_size):
        query = self.session.query(Post)
        if search is not None and len(search) > 2:
            query = query.filter(Post.title.like("%{0}%".format(search)))
        offset = (page-1) * page_size
        return query.limit(page_size).offset(offset).all()

    def count(self, search):
        query = self.session.query(func.count(Post.id))
        if search is not None and len(search) > 2:
            query = query.filter(Post.title.like("%{0}%".format(search)))
        return query.scalar()

    def get(self, id):
        return self.session.query(Post).get(id)

    def get_by_user_id(self, id, user_id):
        return self.session.query(Post).filter_by(id=id, user_id=user_id).first()

    def add(self, title, body, user):
        post = Post(title=title, body=body, author=user)
        self.session.add(post)
        self.session.commit()

    def update(self, post_id, title, body, user_id):
        self.session.query(Post).filter_by(id=post_id).update({'title': title, 'body': body, 'user_id': user_id})
        self.session.commit()

    def delete(self, post_id):
        self.session.query(Post).filter_by(id=post_id).delete()
        self.session.commit()

    def is_unique_post_title(self, title):
        post = self.session.query(Post).filter_by(title=title).first()
        return not post
