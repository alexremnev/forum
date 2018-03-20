from sqlalchemy import Column, Integer, String, DateTime

from app import db


def dump_datetime(value):
    """Deserialize datetime object into string form for JSON processing."""
    if value is None:
        return None
    return [value.strftime("%Y-%m-%d, %H:%M:%S")]


class Comment(db.Model):
    id = Column(Integer, primary_key=True)
    text = Column(String)
    timestamp = Column(DateTime)
    user_id = Column(Integer, db.ForeignKey('user.id'))
    post_id = Column(Integer, db.ForeignKey('post.id'))

    @property
    def serialize(self):
        """Return object data in serializeable format"""
        return {
            'id': self.id,
            'text': self.text,
            'timestamp': dump_datetime(self.timestamp),
            'author': self.author.username
        }
