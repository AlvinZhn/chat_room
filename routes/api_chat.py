# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from flask import (
    Blueprint,
    request,
    jsonify,
)
from routes.socket_chat_events import online_user as user_list

chat_room_api = Blueprint('chat_room_api', __name__)


@chat_room_api.route('/api/chat/user')
def online_user():
    room = request.args.get('room')
    return jsonify(user_list[room])
