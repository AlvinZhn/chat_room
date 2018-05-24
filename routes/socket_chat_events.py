# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from flask import session
from flask_socketio import (
	emit,
	join_room,
	leave_room,
	SocketIO,
)

socketio = SocketIO()

index_pool = []
online_user = {
	'Main': {},
	'Game': {},
	'Else': {},
}


def get_index():
	for i in range(1, 1000):
		if i not in index_pool:
			index_pool.append(i)
			return str(i).zfill(3)
	return 'Error'


def pop_index(name):
	user_id = session.get('user_id')
	if user_id is None:
		index = int(name[6:-1])
		index_pool.remove(index)


def get_name():
	user_id = session.get('user_id')
	if user_id is None:
		index = get_index()
		name = 'Guest[{}]'.format(index)
		session['name'] = name
	return session.get('name')


@socketio.on('join', namespace='/chat')
def join(data):
	room = data['room']
	join_room(room)
	session['room'] = room
	name = get_name()
	message = 'User: ({}) has joined us'.format(name)

	id = session.get('user_id', name[:-1].replace('[', '-'))
	username = session.get('user_name', name)
	user_img = session.get('user_img', '/static/img/guest.png')
	user_info = dict(
		id=id,
		username=username,
		name=name,
		user_img=user_img,
	)
	online_user[room][id] = user_info
	d = dict(
		status='join',
		message=message,
		user_info=user_info,
	)
	emit('status', d, room=room)


@socketio.on('send', namespace='/chat')
def send(data):
	room = session.get('room')
	name = session.get('name')
	message = data.get('message')
	formatted = '{} : {}'.format(name, message)
	d = dict(
		message=formatted,
	)
	emit('message', d, room=room)


@socketio.on('leave', namespace='/chat')
def leave():
	room = session.get('room')
	leave_room(room)
	name = session.get('name')

	id = session.get('user_id', name[:-1].replace('[', '-'))
	online_user[room].pop(id)

	d = dict(
		status='leave',
		message='{} has left the room.'.format(name),
		id=id,
	)
	pop_index(name)
	emit('status', d, room=room)
