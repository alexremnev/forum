import datetime

from app.models.comment import Comment


class CommentService:

    def __init__(self, session):
        self.session = session

    def add(self, text, post_id, user_id):
        comment = Comment(text=text, timestamp=datetime.datetime.utcnow(), user_id=user_id,
                          post_id=post_id)
        self.session.add(comment)
        self.session.commit()
