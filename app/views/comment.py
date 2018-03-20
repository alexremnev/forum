from flask import request, jsonify, current_app

from app import app
from app.services import commentService


@app.route('/_get_comments', methods=['GET'])
def get_comments():
    comments_count = request.args.get('count', 0, type=int)
    post_id = request.args.get('post_id', 0, type=int)
    page_size = current_app.config['COMMENT_PER_PAGE']
    comments = commentService.list(post_id, comments_count, page_size)
    return jsonify([comment.serialize for comment in comments])
