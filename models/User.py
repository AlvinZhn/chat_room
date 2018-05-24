# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""
from models import Model
import hashlib


def salted_password(password, salt='someSaltHere'):
    salted = password + salt
    hashed = hashlib.sha256(salted.encode('ascii')).hexdigest()
    return hashed


class User(Model):
    def __init__(self, form):
        Model.__init__(self, form)
        self.username = form.get('username', '')
        self.password = salted_password(form.get('password', ''))
        self.signature = form.get('signature', '这家伙很懒，什么个性签名都没有留下。')
        self.user_image = form.get('user_image', '')
        self.role = form.get('role', 2)

    @staticmethod
    def validate_login(username, password):
        u = User.find_by(username=username)
        return u is not None and u.password == salted_password(password)

    def validate_register(self):
        return len(self.username) > 2 and len(self.password) > 2

    @staticmethod
    def guest():
        form = dict(
            id=-1,
            username='游客',
        )
        u = User.new(form)
        return u
