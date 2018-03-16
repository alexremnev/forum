from flask_sqlalchemy_session import flask_scoped_session
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import app
from app.services.user_service import UserService
from app.services.role_service import RoleService
from app.services.post_service import PostService
from .comment_service import CommentService

engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
session_factory = sessionmaker(bind=engine)
session = flask_scoped_session(session_factory, app)

commentService = CommentService(session)
postService = PostService(session)
roleService = RoleService(session)
userService = UserService(session, roleService)
