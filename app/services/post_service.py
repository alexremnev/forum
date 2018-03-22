from sqlalchemy import func

from app.models.post import Post
from app.services.utils import commit_required


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

    @commit_required
    def add(self, title, body, user):
        post = Post(title=title, body=body, author=user)
        self.session.add(post)

    @commit_required
    def update(self, post_id, **kwargs):
        self.session.query(Post).filter_by(id=post_id).update(kwargs)

    @commit_required
    def delete(self, post_id):
        self.session.query(Post).filter_by(id=post_id).delete()
        self.session.commit()

    def is_unique_title(self, title):
        post = self.session.query(Post).filter_by(title=title).first()
        return not post
