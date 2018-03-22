import datetime

from app.models.comment import Comment
from app.services.utils import commit_required


class CommentService:

    def __init__(self, session):
        self.session = session

    @commit_required
    def add(self, text, post_id, user_id):
        comment = Comment(text=text, timestamp=datetime.datetime.utcnow(), user_id=user_id,
                          post_id=post_id)
        self.session.add(comment)

    def list(self, post_id, offset, page_size):
        return self.session.query(Comment).filter_by(post_id=post_id).limit(page_size) \
            .offset(offset).all()
