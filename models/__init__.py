# -*- coding: utf-8 -*-
"""
@Author: 'Zhang'
"""

import json

import time


def save(data, path):
	"""
	将用户的注册信息(list or dict)写入文件
	"""
	s = json.dumps(data, indent=2, ensure_ascii=False)
	with open(path, 'w+', encoding='utf-8') as f:
		f.write(s)


def load(path):
	"""
	从文件中读取已有的注册用户信息，转化为dict or list
	"""
	with open(path, 'r', encoding='utf-8') as f:
		s = f.read()
		return json.loads(s)


def formatted_time(unix_time):
	time_format = '%Y/%m/%d %H:%M:%S'
	return time.strftime(time_format, time.localtime(unix_time))


class Model(object):
	def __init__(self, form):
		# 从json文件中获取id值，没有则为None
		self.id = form.get('id', None)
		self.created_time = form.get('created_time', 0)
		self.updated_time = form.get('updated_time', 0)

	# 获取对应子类数据文件路径
	@classmethod
	def db_path(cls):
		classname = cls.__name__
		path = 'db/{}.txt'.format(classname)
		return path

	# 在对应子类下传入表单中的数据新建实例
	@classmethod
	def new(cls, form):
		m = cls(form)
		timestamp = formatted_time(int(time.time()))
		m.created_time = timestamp
		m.updated_time = timestamp
		m.save()
		return m

	@classmethod
	def _new_from_dict(cls, d):
		m = cls({})
		for k, v in d.items():
			setattr(m, k, v)
		return m

	@classmethod
	def all(cls):
		path = cls.db_path()
		models = load(path)
		ms = [cls._new_from_dict(m) for m in models]
		return ms

	def save(self):
		# 获取该类下已有的所有实例(list)
		models = self.all()
		if self.id is None:
			if len(models) == 0:
				self.id = 1
			else:
				self.id = models[-1].id + 1
			models.append(self)
		else:
			for i, m in enumerate(models):
				if m.id == self.id:
					models[i] = self
					break
		l = [m.__dict__ for m in models]
		path = self.db_path()
		save(l, path)

	@classmethod
	def update_time(cls, id):
		m = cls.find_by(id=id)
		m.updated_time = formatted_time(int(time.time()))
		return m

	@classmethod
	def remove(cls, id):
		titles = cls.all()
		index = -1
		for i, m in enumerate(titles):
			if m.id == id:
				index = i
				break
		if index != -1:
			o = titles.pop(index)
			l = [t.__dict__ for t in titles]
			path = cls.db_path()
			save(l, path)
			return o

	@staticmethod
	def valid_kwargs(model, kwargs):
		for key, value in kwargs.items():
			if value != getattr(model, key):
				return False
		return True

	@classmethod
	def find_by(cls, **kwargs):
		instances = cls.all()
		for model in instances:
			exist = cls.valid_kwargs(model, kwargs)
			if exist:
				return model
		return None

	@classmethod
	def find_all(cls, **kwargs):
		model_list = []
		instances = cls.all()
		kw_numbers = len(kwargs)
		for el in instances:
			flag = False
			for i in range(kw_numbers):
				key = list(kwargs.keys())[i]
				if getattr(el, key) == kwargs[key]:
					flag = True
				else:
					flag = False
			if flag:
				model_list.append(el)
		return model_list

	def json(self):
		"""
		返回当前 model 的字典表示
		"""
		d = self.__dict__
		return d

	@staticmethod
	def all_json(data_list):
		jsons = [data.json() for data in data_list]
		return jsons

	# 赋予实例可以调用的特性，
	def __repr__(self):
		classname = self.__class__.__name__
		properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
		s = '\n'.join(properties)
		return '< {}\n{} >\n'.format(classname, s)
