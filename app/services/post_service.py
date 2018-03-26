from sqlalchemy import func
from sqlalchemy.orm import subqueryload, joinedload

from app import cache, Comment
from app.models.post import Post
from app.services.utils import commit_required


class PostService:

    def __init__(self, session):
        self.session = session

    @cache.memoize(10)
    def list(self, search, page, page_size):
        query = self.session.query(Post)
        if search is not None and len(search) > 2:
            query = query.filter(Post.title.like("%{0}%".format(search)))
        offset = (page - 1) * page_size
        return query.options(joinedload(Post.author)).limit(page_size).offset(offset).all()

    @cache.memoize(10)
    def count(self, search):
        query = self.session.query(func.count(Post.id))
        if search is not None and len(search) > 2:
            query = query.filter(Post.title.like("%{0}%".format(search)))
        return query.scalar()

    @cache.cached(timeout=10)
    def get(self, id):
        return self.session.query(Post) \
            .options(subqueryload('author'), joinedload('comments').subqueryload(Comment.author)) \
            .get(id)

    @cache.cached(timeout=10)
    def get_by_user_id(self, id, user_id):
        return self.session.query(Post).filter_by(id=id, user_id=user_id).first()

    @commit_required
    def add(self, title, body, user):
        post = Post(title=title, body=body, author=user)
        cache.delete_memoized(self.list)
        cache.delete_memoized(self.count)
        self.session.add(post)

    @commit_required
    def update(self, post_id, **kwargs):
        self.session.query(Post).filter_by(id=post_id).update(kwargs)

    @commit_required
    def delete(self, post_id):
        self.session.query(Post).filter_by(id=post_id).delete()
        cache.delete_memoized(self.list)
        cache.delete_memoized(self.count)

    def is_unique_title(self, title):
        post = self.session.query(Post).filter_by(title=title).first()
        return not post
