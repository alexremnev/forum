from app import db
from .user_service import UserService
from .role_service import RoleService
from .post_service import PostService
from .comment_service import CommentService

session = db.session

commentService = CommentService(session)
postService = PostService(session)
roleService = RoleService(session)
userService = UserService(session, roleService)
