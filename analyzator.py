__author__ = "KolyazovKA"

import string

from colorama import Fore, Style

from Reader import Reader, br_file_path, file_path
from prettytable import PrettyTable as pt
import re

"""
Список необходимых функций:
* проверка функций (выполнено)
* проверка комментариев (выполнено)
* проверка скобок (выполнено)
* проверка операторов (выполнено)
* проверка чисел (выполнено)
* Вывод таблицы лексем
"""

SP_CHAR = [
	";", "{", "}", "(", ")"
]

OPERATORS = [
	"+", "-", "*", "/", ":=",
]

NUMBS = [
	"1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F", "-",
]



def fill_vars(vars):
	"""Заполнение массива символов переменных"""
	characters = string.ascii_letters + string.digits + '_'
	for i in characters:
		vars.append(i)


class Analyzator:
	def __init__(self, data):
		self.broken_numbs = []
		self.input_data = data
		self.vars_of_str = []
		self.broken_vars = []
		self.numbs_of_str = []
		self.oper_of_str = []
		self.broken_oper = []
		self.another_broken_chars =[":", "="]
		self.err_message = []

		#Инициализация таблицы
		self.table = pt(['Тип лексемы', 'Строка', 'Позиция', 'Значение'])

		#Сценарий проверки
		self.check_vars()
		self.check_comments()
		self.check_brackets()
		self.check_number()
		self.check_operator()
		self.check_assig_operator()

		# Вывод таблицы
		self.output_table()

		#Вывод ошибок
		self.output_errors()


	def output_table(self):
		"""Выводит таблицу лексем"""
		for numb_str in range(len(self.input_data)):
			position = 1
			for expr in range(len(self.input_data[numb_str + 1])):
				expr_chars = re.split(" ", self.input_data[numb_str + 1][expr])
				for chars in expr_chars:
					self.read_chars(chars, numb_str, pos=position)
					position += 1
		print(self.table)

	def read_chars(self, chars, numb_str, pos):
		flag = True
		flag_str = True
		for operator in SP_CHAR:
			if operator in chars and flag_str:
				if chars not in self.another_broken_chars:
					other = chars.replace(operator, "")
					string = self.join_array_elements(self.input_data[numb_str + 1])
					position = pos
					self.read_chars(other, numb_str, position)
					position += 1
					self.fill_table(numb_str + 1, position, operator)
					flag_str = False
					flag = False
				else:
					flag = False
		if flag:
			string = self.join_array_elements(self.input_data[numb_str + 1])
			position = pos
			if chars not in self.another_broken_chars:
				self.fill_table(numb_str + 1, position, chars)

	def fill_table(self, numb_str, position, char):
		if char in self.vars_of_str and ['Идентификатор', numb_str, position, char] not in self.table:
			self.table.add_row(['Идентификатор', numb_str, position, char])
		elif char in self.numbs_of_str and ['Число', numb_str, position, char] not in self.table:
			self.table.add_row(['Число', numb_str, position, char])
		elif char != "" and char in "(" and ['Открывающая круглая скобка', numb_str, position, char] not in self.table:
			self.table.add_row(['Открывающая круглая скобка', numb_str, position, char])
		elif char != "" and char in ")" and ['Закрывающая круглая скобка', numb_str, position, char] not in self.table:
			self.table.add_row(['Закрывающая круглая скобка', numb_str, position, char])
		elif char != "" and char in "{" and ['Открывающая фигурная скобка', numb_str, position, char] not in self.table:
			self.table.add_row(['Открывающая фигурная скобка', numb_str, position, char])
		elif char != "" and char in "}" and ['Закрывающая фигурная скобка', numb_str, position, char] not in self.table:
			self.table.add_row(['Закрывающая фигурная скобка', numb_str, position, char])
		elif char != "" and char in ":=" and ['Оператор присваивания', numb_str, position, char] not in self.table:
			self.table.add_row(['Оператор присваивания', numb_str, position, char])
		elif char != "" and char in "*" and ['Оператор умножения', numb_str, position, char] not in self.table:
			self.table.add_row(['Оператор умножения', numb_str, position, char])
		elif char != "" and char in "/" and ['Оператор деления', numb_str, position, char] not in self.table:
			self.table.add_row(['Оператор деления', numb_str, position, char])
		elif char != "" and char in "+" and ['Оператор сложения', numb_str, position, char] not in self.table:
			self.table.add_row(['Оператор сложения', numb_str, position, char])
		elif char != "" and char in "-" and ['Оператор вычитания', numb_str, position, char] not in self.table:
			self.table.add_row(['Оператор вычитания', numb_str, position, char])
		elif char != "" and char in ";" and ['Точка с запятой', numb_str, position, char] not in self.table:
			self.table.add_row(['Точка с запятой', numb_str, position, char])
	def remove_content_inside_braces(self, string):
		if string[0] == "{" and string[-1] == "}":
			return "{}"
		return string

	def join_array_elements(self, array):
		return " ".join([str(element) for element in array])
	def get_word_position(self, sentence, word):
		words = sentence.split()  # Разделяем строку на слова
		for index, w in enumerate(words, 1):
			if w == word:
				return str(index)

	def check_number(self):
		"""Проверяет правильность написания шестнадцатеричных чисел"""

		for numb_str in range(len(self.input_data)):
			for expr in range(len(self.input_data[numb_str + 1])):
				expr_chars = re.split(" ", self.input_data[numb_str + 1][expr])
				for chars in expr_chars:
					#Удаление лишнего
					chars = self.prepare_string_for_hex_numb(chars)
					if chars == " ":
						continue
					if chars == "=":
						continue

					#Проверка числа
					flag = True
					for i in chars:
						if i not in NUMBS:
							flag = False
							if i not in self.broken_numbs:
								self.broken_numbs.append(chars)
							self.err_message.append( f"Ошибка в написании шестнадцатеричного числа {chars}"
							      f"на строке номер {numb_str + 1} в выражении {expr + 1}\n")
							break
					if flag:
						self.numbs_of_str.append(chars)


	def prepare_string_for_hex_numb(self, chars):
		if "{" in chars or "}" in chars:
			return " "
		if chars in OPERATORS:
			return " "
		if chars in SP_CHAR:
			return " "
		if ";" in chars:
			chars = chars.replace(";", "")
		if "(" in chars:
			chars = chars.replace("(", "")
		if ")" in chars:
			chars = chars.replace(")", "")
		if chars in self.vars_of_str or chars in self.broken_vars:
			return " "
		return chars

	def print_vars(self):
		print(f"vars: {self.vars_of_str}")

	def append_var(self, var):
		self.vars_of_str.append(var)

	def sort_vars(self):
		self.vars_of_str.sort()

	def check_brackets(self):
		"""Проверяет соответсвие открытых и закрытых скобок"""
		for i in range(len(self.input_data)):
			for j in range(len(self.input_data[i+1])):
				open_br = 0
				close_br = 0
				for k in range(len(self.input_data[i+1][j])):
					if self.input_data[i+1][j][k] == "(": open_br += 1
					if self.input_data[i+1][j][k] == ")": close_br += 1
				if open_br > close_br:
					self.err_message.append(f"Не хватает {open_br - close_br} закрывающих "
					                        f"скобок на строке {i+1} в выражении {j+1}\n")
				elif close_br > open_br:
					self.err_message.append(f"{close_br - open_br} закрывающих скобок лишние "
					      f"на строке {i+1} в выражении {j+1}\n")
				else:
					continue

	def check_comments(self):
		"""Проверка правильности написания комментариев"""
		for i in range(len(self.input_data)):
			for j in range(len(self.input_data[i + 1])):
				open_char = None
				close_char = None
				for char in range(len(self.input_data[i + 1][j])):
					if self.input_data[i + 1][j][char] == "{":
						open_char = char
					if self.input_data[i + 1][j][char] == "}":
						close_char = char
				if (open_char is None and close_char is None) \
						or (open_char is not None and close_char is not None):
					continue
				else:
					err_str = re.split(" ", self.input_data[i+1][j])
					err_comment = " "
					for asd in err_str:
						if "{" in asd or "}" in asd:
							err_comment = asd
					self.another_broken_chars.append(err_comment)
					self.err_message.append(f"Ошибка в написании комментария "
					                        f"на строке {i + 1}: \n\t{err_comment}\n "
					                        f"не закрытая (не открытая) фигурная скобка\n")

	def check_vars(self):
		"""Заполнение массива переменных и их проверка"""
		for i in range(len(self.input_data)):
			for j in range(len(self.input_data[i + 1])):
				var = re.split(" ", self.input_data[i + 1][j])
				for char in var:
					if char[0] == "{" or char[0] in self.vars_of_str:
						continue
					if not char[0].isalpha() and not char[0] == "_":
						# self.broken_vars.append(char)
						# self.err_message.append(f"Ошибка в наименовании переменной {char} "
						#       f"на строке {i + 1} в выражении {j + 1}\n")
						continue

					self.append_var(char)
		self.sort_vars()

	def check_operator(self):
		for numb_str in range(len(self.input_data)):
			for expr in range(len(self.input_data[numb_str + 1])):
				expr_chars = re.split(" ", self.input_data[numb_str + 1][expr])
				for chars in expr_chars:
					for char in chars:
						if (char in SP_CHAR or char in OPERATORS) and char not in self.oper_of_str:
							self.oper_of_str.append(char)

	def output_errors(self):
		if len(self.err_message) != 0:
			print(Fore.RED + Style.BRIGHT + "Список ошибок:" + Style.RESET_ALL)
		for i in self.err_message:
			print(Fore.RED + f"{self.err_message.index(i) + 1}:" + i + Style.RESET_ALL)

	def check_assig_operator(self):
		for numb_str in range(len(self.input_data)):
			for expr in range(len(self.input_data[numb_str + 1])):
				if ":=" in self.input_data[numb_str + 1][expr]:
					parts = self.input_data[numb_str + 1][expr].split(":=")
					if len(parts) == 2 and parts[0].strip().isidentifier() and parts[1].strip() and ":=" not in self.oper_of_str:
						self.oper_of_str.append(":=")
					continue
				if "{" not in self.input_data[numb_str + 1][expr] or "}" not in self.input_data[numb_str + 1][expr]:
					self.err_message.append(f"Ошибка в написании оператора присваивания "
		                        f"на строке {numb_str + 1} в выражении {expr + 1}\n")


def lecs_analysator():
	reader = Reader(file_path)
	print(f"\n\n\t\t\t\t\t\tТаблица лексем")
	analyzator = Analyzator(reader.lines)
	print()


if __name__ == "__main__":
	lecs_analysator()
