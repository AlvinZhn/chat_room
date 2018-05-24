# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
import config

from flask import Flask, render_template
from flask_session import Session

from routes.socket_chat_events import socketio
from routes.api_chat import chat_room_api

from routes.routes_static import main as index_view


def register_routes(app):
	app.register_blueprint(chat_room_api)

	app.register_blueprint(index_view)


def filter_location(path):
	"""
	jinja2 filter
	Formats path
	"""
	location = path.split('/')[1].capitalize()
	if location == '':
		return 'Index'
	return path.split('/')[1].capitalize()


def configured_app():
	app = Flask(__name__)

	register_routes(app)
	# load config from config file
	app.config.from_object(config)
	Session(app)

	# custom jinja2 filter
	app.jinja_env.filters["location"] = filter_location

	# init socketio
	socketio.init_app(app)

	return app


if __name__ == '__main__':
	app = configured_app()

	# 自动 reload jinja
	app.config['TEMPLATES_AUTO_RELOAD'] = True
	app.jinja_env.auto_reload = True
	# 关闭 js 静态缓存
	app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

	config = dict(
		host='0.0.0.0',
		port=3000,
		debug=True,
	)
	socketio.run(app, **config)
