#-*-coding:utf8;-*-
import config
import sqlitep
import re

def search(message, stolb):
	searchText = DefSqlInject(message.text).upper()
	if searchText == "":
		return ["error","Запрос пустой, при запросе учитываются только буквы и цифры"]
	if len(searchText) <= 1:
		return ["error","Маленький запрос, минимум два символа (учитываются только буквы и цифры)"]
	print("\n"+ str(message.chat.id ) +" Имя: " + str(message.chat.first_name ) + " Ник: " + str(message.chat.username)+ "  Раздел: " + stolb )
	db_conn = sqlitep.SQLighter(config._databaseName)
	ret= str(db_conn.find(searchText, stolb))
	db_conn.close()
	if str(ret) ==  "[]":
		return ["error","Я везде посмотрел, но того, что ты мне назвал - нет \nЕсли ты считаешь, что это должно быть - напиши в чат @book_it"]
	
	retText = ret.split("),")
	returnList = []
	for i in retText:
		returnList.append(i)
	a = 0
	for i in returnList:
		retReplace = str(i).replace("[", "").replace("]","").replace("(","").replace(")","").replace("'","")
		retMsg = retReplace.split(",")
		returnList[a] = retMsg
		a += 1
	return returnList
	
def addDB(message):
	if message.chat.id == config._FATHERid:
		if message.content_type == 'document':
			if message.forward_from_chat != None:
				#forMsgId номер сообщения на канале, подставляя его к ссылке канала можно получить полную ссылку к посту
				forMsgId = message.forward_from_message_id
				linkOnChannel = "https://t.me/bzd_channel/"
				channelId = -1001075040616
				fileName = message.document.file_name
				fileSize = message.document.file_size
				#Описание к файлу, из него убираем двойные кавычки, одинарные кавычки, запятые, и режем это всё по символу переноса строк
				captionSplit = message.caption.upper().replace("\"", "").replace("'","").replace(",", "").split("\n")
				print(str(captionSplit))
				leng = len(captionSplit)
				tag = captionSplit[0]
				#Если язык есть, значит ищем название и автора в третьем пункте, если нет - во втором
				p = 2
				if captionSplit[1][0] == "[":
					language = captionSplit[1]
				else:
					language = "#?"
					p = 1
					
				authorNameSplit = captionSplit[p].split("|")
				if len(authorNameSplit) == 2:
					author = authorNameSplit[0]	
					name = authorNameSplit[1]
				elif len(authorNameSplit) == 1:
					author = "#?"
					name = authorNameSplit[0]
				else:
					return "error split author or name"
					
				link = linkOnChannel + str(forMsgId)
				#Следующий цикл просматривает оставшиеся строки в поисках даты
				try:
					i = 1
					while i <= leng - 1:
						if captionSplit[i] != "":
							if captionSplit[i][0] == "#":
								age = captionSplit[i]
								break
							elif i >= leng-1:
								age = "#?"
								break
							else:
								i = i+1
						elif i >= leng - 1:
							age = "#?"
							break
						else:
							i = i+1
						if i == leng-1:
							age = "#?"
				except Exceprion as e:
					print ("\nError AddNew: " + str(e))
					age = "#?"
					
				print("\n"+"author: "+author+"	name: "+name+"	tag: " + tag + "	age: " + age + "	link: " + link + "	language: " + language + "\n")
				db_conn = sqlitep.SQLighter(config._databaseName)
				db_conn.addNew(author, name,tag,age,link,language)
				db_conn.close()
				return "ok"
				
#Создать таблицу, имя захардкожено
def createTable():
	db_conn = sqlitep.SQLighter(config._databaseName)
	ret = db_conn.createBookTable()
	db_conn.close()
	return ret
	
#Выдать всю базу
def selectAll():
	db_conn = sqlitep.SQLighter(config._databaseName)
	ret = db_conn.select_all()
	db_conn.close()
	return ret
	
#Подсчет строк в базе
def countRows():
	db_conn = sqlitep.SQLighter(config._databaseName)
	ret = db_conn.count_rows()
	db_conn.close()
	return ret
	
#Защита от sql инжектов, режет всё, кроме букв и цифр, в местах разрыва ставит %, оператор LIKE с ним лучше ищет (появляется возможность пропускать слова
def DefSqlInject(text):
	l = list(filter(None, re.split('\W|_', text)))
	ret = "%".join(l)
	return ret
	
