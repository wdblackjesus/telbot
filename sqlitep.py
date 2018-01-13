import sqlite3 

class SQLighter: 

	def __init__(self, database):
		self.connection = sqlite3.connect(database) 
		self.cursor = self.connection.cursor() 
	
	def find(self, text, stolb):
		sqlex = "SELECT * FROM book WHERE {stolb} LIKE '%{text}%'".format(stolb=stolb, text=text)
		with self.connection:
			ret = self.cursor.execute(sqlex).fetchall()
			print("\nЗапрос: " + str(text))
			print ("\nдлина ответа: "+str(len(ret)))
			return ret
			
#Создать новую таблицу, автоматически вместе с ней создается и новая база
	def createBookTable (self):
		try:
			#sqlex = 'INSERT INTO book (author, name, tag, age, link) VALUES ("{auth}","{nam}","{ta}","{ag}","{lnk}");'.format(auth=author,nam=name,ta=tag,ag=age,lnk=link)
			sqlex = "CREATE TABLE book(Id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL , author TEXT, name TEXT, tag TEXT, age TEXT, link TEXT, language TEXT)"
			print(sqlex)
			with self.connection:
				s = self.cursor.execute(sqlex)
				self.connection.commit()
				
				return "ok: создана новая таблица"
		except Exception as e:
			print ("ОШИБКА СОЗДАНИЯ НОВОЙ ТАБЛИЦЫ\n" + str(e))
			return "Ошибка создания новой таблицы"
	

	def addNew(self, author,name,tag,age,link, language):
		try:
			sqlex = 'INSERT INTO book (author, name, tag, age, link, language) VALUES ("{auth}","{nam}","{ta}","{ag}","{lnk}","{lang}");'.format(auth=author,nam=name,ta=tag,ag=age,lnk=link,lang=language)
			#sqlex = "CREATE TABLE book(Id INT NOT NULL auto_increment primary key , author TEXT, name TEXT, tag TEXT, age TEXT, link TEXT)"
			print(sqlex)
			with self.connection:
				s = self.cursor.execute(sqlex)
				self.connection.commit()
				return "Ok: Добавлена новая запись"
		except Exception as e:
			print ("ОШИБКА ПРИ ДОБАВЛЕНИИ ЗАПИСИ! \n" + str(e))
			return "Ошибка при добавлении записи"
	
	def select_all(self):
	#""" Получаем все строки """ 
		with self.connection: 
			return self.cursor.execute('SELECT * FROM book').fetchall() 


	def count_rows(self): 
	#""" Считаем количество строк """ 
		with self.connection: 
			result = self.cursor.execute('SELECT * FROM book').fetchall() 
			return len(result) 

	def close(self): 
	#""" Закрываем текущее соединение с БД """ 
		self.connection.close()
    
