__author__ = "KolyazovKA"

import re

file_path = 'WithoutErrors.txt'
br_file_path = 'WithErrors.txt'


class Reader:
	def __init__(self, f_path):
		self.file_path = f_path
		self.file_info = None
		self.data = None
		self.line_without_comments = []
		self.lines = {}

		self.read_file()

	def read_file(self):
		"""
		Генерируем из информации из файла словарь с номерами строк и их содержимым
		:return:
		"""
		# Читаем файл
		with open(self.file_path, 'r') as file:
			self.file_info = file.read()
		# Делим информацию на строки
		# self.data = self.get_line()
		# # Удаляем комментарии
		# self.line_without_comments = self.delete_comments()
		# print(self.line_without_comments)
		# Составляем словарь из номеров строк и значений
		self.fill_lines()
		self.lines = self.separate_comments(self.lines)

	def get_line(self):
		"""
		Делим информацию из файла по строкам
		:return:
		"""
		data = self.file_info
		return re.split('\n', data)

	@staticmethod
	def separate_comments(dictionary):
		result = {}
		for key, value in dictionary.items():
			separated_value = []
			for item in value:
				# Используем регулярное выражение для разделения строки на комментарии и остальной текст
				split_item = re.split(r'(\{.*?\})', item)
				separated_value.extend(split_item)
			result[key] = [item.strip() for item in separated_value if item.strip() != '']

		return result

	def fill_lines(self):
		"""
		Заполняем словарь строк
		:return:
		"""
		lines = []
		lines = self.get_line()
		for i in range(len(lines)):
			if not self.have_multiline(lines[i]):
				self.lines[i + 1] = [lines[i]]
			else:
				for line in self.split_by_semicolon(lines[i]):
					self.lines[i + 1] = self.split_by_semicolon(lines[i])

	@staticmethod
	def have_multiline(data):
		"""
		Проверка на несколько выражений в строке
		:param data:
		:return:
		"""
		return len(re.split(';+', data)) > 2

	@staticmethod
	def split_by_semicolon(data):
		"""
		Делим строки на подстроки по точке с запятой
		:param data:
		:return:
		"""
		line = re.split(';+', data)

		for i in range(len(line)):
			if not line[i] == '':
				line[i] = line[i] + ";"
			else:
				line.pop(i)
		return line


def main():
	"""Проверка работоспособности методов"""
	reader = Reader(br_file_path)
	print(reader.lines)


if __name__ == "__main__":
	main()
